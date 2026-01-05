<!-- src\views\Home.vue -->
<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";
import RestaurantCard from "../components/RestaurantCard.vue";
import SearchBox from "../components/SearchBox.vue";

const restaurants = ref([]);
const loading = ref(true);

onMounted(async () => {
    try {
        const { data } = await api.get("/restaurants");
        restaurants.value = data;
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="min-h-screen bg-white text-gray-900 font-sans">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">

            <!-- Header con búsqueda integrada -->
            <header class="mb-12 pt-8">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
                    <div>
                        <h1 class="text-3xl font-light tracking-tight mb-2">Puno</h1>
                        <p class="text-[10px] font-mono uppercase tracking-[0.2em] text-gray-400">
                            Selección de Restaurantes
                        </p>
                    </div>
                    
                    <!-- SearchBox en una posición más prominente -->
                    <div class="md:w-96">
                        <SearchBox />
                    </div>
                </div>

                <!-- Línea divisora para separar header del contenido -->
                <div class="border-t border-gray-100 pt-8">
                    <h2 class="text-lg font-medium text-gray-900 mb-6">
                        Restaurantes destacados
                    </h2>
                </div>
            </header>

            <!-- Contenido principal -->
            <main>
                <div v-if="loading" class="animate-pulse space-y-12">
                    <div v-for="n in 6" :key="n" class="h-24 bg-gray-50 w-full rounded-sm"></div>
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
                    <RestaurantCard v-for="r in restaurants" :key="r.locationId" :restaurant="r" />
                </div>
            </main>
        </div>
    </div>
</template>