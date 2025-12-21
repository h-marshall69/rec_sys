<!-- src\views\Home.vue -->
<script setup>
import { onMounted, ref } from "vue";
import api from "../services/api";
import RestaurantCard from "../components/RestaurantCard.vue";

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
        <div class="max-w-5xl mx-auto px-6 py-16">

            <header class="mb-20">
                <h1 class="text-4xl font-light tracking-tight mb-2">Puno</h1>
                <p class="text-gray-400 font-mono text-sm uppercase tracking-widest">
                    Selección de Restaurantes
                </p>
            </header>

            <div v-if="loading" class="animate-pulse space-y-12">
                <div v-for="n in 6" :key="n" class="h-24 bg-gray-50 w-full rounded-sm"></div>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-16">
                <RestaurantCard v-for="r in restaurants" :key="r.locationId" :restaurant="r" />
            </div>
        </div>
    </div>
</template>