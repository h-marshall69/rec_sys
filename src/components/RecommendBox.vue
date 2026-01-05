<!-- src\components\RecommendBox.vue -->
<script setup>
import { ref } from "vue";
import api from "../services/api";

const query = ref("");
const results = ref([]);
const loading = ref(false);
const showSuggestions = ref(true);

const suggestions = [
  "Restaurantes románticos para una cita",
  "Lugares con comida vegana",
  "Sitios para desayunar cerca",
  "Restaurantes con terraza",
  "Comida mexicana auténtica",
  "Pizzerías artesanales",
  "Sushi fresco de calidad",
  "Hamburguesas gourmet",
  "Cafeterías con buen ambiente",
  "Restaurantes para grupos grandes"
];

const recommend = async () => {
    if (!query.value.trim()) return;
    
    showSuggestions.value = false;
    loading.value = true;
    results.value = [];

    try {
        const { data } = await api.post("/recommend", {
            query: query.value,
            top_n: 10,
        });
        results.value = data;
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
};

const useSuggestion = (suggestionText) => {
    query.value = suggestionText;
    recommend();
};

const resetSearch = () => {
    query.value = "";
    results.value = [];
    showSuggestions.value = true;
};
</script>

<template>
    <div class="w-full max-w-xl mx-auto font-sans text-gray-900">

        <!-- Barra de búsqueda -->
        <div class="flex items-end gap-4 mb-5">
            <div class="relative flex-1">
                <input 
                    v-model="query" 
                    @keyup.enter="recommend" 
                    @focus="showSuggestions = true"
                    placeholder="¿Qué tipo de restaurante buscas?"
                    class="w-full bg-transparent border-b border-gray-300 py-2 text-lg focus:border-black focus:outline-none placeholder-gray-400 transition-colors pr-8" 
                />
                <!-- Botón para resetear -->
                <button 
                    v-if="!showSuggestions && (query || results.length > 0)"
                    @click="resetSearch"
                    class="absolute right-0 bottom-2 text-gray-400 hover:text-gray-600 transition-colors"
                    title="Nueva búsqueda"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm.707-10.293a1 1 0 00-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L9.414 11H13a1 1 0 100-2H9.414l1.293-1.293z" clip-rule="evenodd" />
                    </svg>
                </button>
            </div>
            <button 
                @click="recommend" 
                :disabled="loading"
                class="text-sm font-medium tracking-wide hover:text-gray-500 disabled:text-gray-300 uppercase pb-2 transition-colors"
            >
                {{ loading ? '...' : 'Buscar' }}
            </button>
        </div>

        <!-- Botones de sugerencia -->
        <div v-if="showSuggestions" class="mb-8">
            <p class="text-sm text-gray-500 mb-3">¿No sabes qué buscar? Prueba con:</p>
            <div class="flex flex-wrap gap-2">
                <button
                    v-for="(suggestion, index) in suggestions"
                    :key="index"
                    @click="useSuggestion(suggestion)"
                    class="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-300"
                >
                    {{ suggestion }}
                </button>
            </div>
        </div>

        <!-- Resultados -->
        <div v-if="!showSuggestions" class="space-y-12">
            <!-- Botón para volver a sugerencias -->
            <div v-if="results.length === 0 && !loading" class="text-center">
                <button 
                    @click="resetSearch"
                    class="text-sm text-gray-500 hover:text-gray-700 underline transition-colors"
                >
                    ← Ver sugerencias de nuevo
                </button>
            </div>

            <!-- Lista de resultados -->
            <div v-for="r in results" :key="r.locationId" class="group">
                <div class="flex justify-between items-baseline mb-3">
                    <h3 class="text-xl font-medium tracking-tight">
                        <router-link :to="`/restaurants/${r.locationId}`" class="hover:underline transition-colors">
                            {{ r.localizedName }}
                        </router-link>
                    </h3>

                    <div class="text-right">
                        <span class="block text-xs text-gray-400 uppercase tracking-wider">Match</span>
                        <span class="text-sm font-mono">{{ (r.final_score * 100).toFixed(0) }}%</span>
                    </div>
                </div>

                <div v-if="r.photos?.length" class="flex gap-1 overflow-x-auto pb-2 scrollbar-hide">
                    <a 
                        v-for="(photo, i) in r.photos" 
                        :key="i" 
                        :href="photo" 
                        target="_blank"
                        class="flex-shrink-0 opacity-90 hover:opacity-100 transition-opacity"
                    >
                        <img 
                            :src="photo" 
                            class="w-24 h-24 object-cover bg-gray-100" 
                            loading="lazy" 
                            alt="" 
                        />
                    </a>
                </div>
                <p v-else class="text-xs text-gray-300 mt-2">Sin imágenes</p>
            </div>
        </div>

        <!-- Sin resultados -->
        <div v-if="!loading && !showSuggestions && query && results.length === 0" 
             class="text-center text-gray-400 text-sm mt-10">
            <p>Sin resultados para "{{ query }}"</p>
            <button 
                @click="resetSearch"
                class="mt-2 text-gray-500 hover:text-gray-700 underline text-sm transition-colors"
            >
                Intentar con otra búsqueda
            </button>
        </div>

    </div>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>