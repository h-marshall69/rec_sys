<!-- src\components\RecommendBox.vue -->
<script setup>
import { ref } from "vue";
import api from "../services/api";

const query = ref("");
const results = ref([]);
const loading = ref(false);

const recommend = async () => {
    if (!query.value.trim()) return;
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
</script>

<template>
    <div class="w-full max-w-xl mx-auto font-sans text-gray-900">

        <div class="flex items-end gap-4 mb-5">
            <input v-model="query" @keyup.enter="recommend" placeholder="Busca un restaurante..."
                class="w-full bg-transparent border-b border-gray-300 py-2 text-lg focus:border-black focus:outline-none placeholder-gray-400 transition-colors" />
            <button @click="recommend" :disabled="loading"
                class="text-sm font-medium tracking-wide hover:text-gray-500 disabled:text-gray-300 uppercase pb-2">
                {{ loading ? '...' : 'Buscar' }}
            </button>
        </div>

        <div class="space-y-12">
            <div v-for="r in results" :key="r.locationId" class="group">

                <div class="flex justify-between items-baseline mb-3">
                    <h3 class="text-xl font-medium tracking-tight">
                        {{ r.localizedName }}
                    </h3>
                    <div class="text-right">
                        <span class="block text-xs text-gray-400 uppercase tracking-wider">Match</span>
                        <span class="text-sm font-mono">{{ (r.final_score * 100).toFixed(0) }}%</span>
                    </div>
                </div>

                <div v-if="r.photos?.length" class="flex gap-1 overflow-x-auto pb-2 scrollbar-hide">
                    <a v-for="(photo, i) in r.photos" :key="i" :href="photo" target="_blank"
                        class="flex-shrink-0 opacity-90 hover:opacity-100 transition-opacity">
                        <img :src="photo" class="w-24 h-24 object-cover bg-gray-100" loading="lazy" alt="" />
                    </a>
                </div>
                <p v-else class="text-xs text-gray-300 mt-2">Sin imágenes</p>
            </div>
        </div>

        <div v-if="!loading && query && results.length === 0" class="text-center text-gray-400 text-sm mt-10">
            Sin resultados.
        </div>

    </div>
</template>

<style scoped>
/* Utilidad para ocultar scrollbar pero permitir scroll */
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>