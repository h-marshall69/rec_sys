<!-- src\views\RestaurantDetail.vue -->
<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const restaurant = ref(null);
const loading = ref(true);

onMounted(async () => {
    try {
        const { data } = await api.get(`/restaurants/${route.params.id}`);
        restaurant.value = data;
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }
});

const goBack = () => router.back();
</script>

<template>
    <div class="min-h-screen bg-white text-gray-900 font-sans pb-20">

        <div v-if="loading" class="max-w-4xl mx-auto p-6 animate-pulse space-y-8 pt-20">
            <div class="h-4 bg-gray-100 w-24 mb-10"></div>
            <div class="h-12 bg-gray-100 w-3/4"></div>
            <div class="h-6 bg-gray-100 w-32"></div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
                <div class="h-64 bg-gray-100 w-full"></div>
                <div class="h-64 bg-gray-100 w-full"></div>
            </div>
        </div>

        <div v-else-if="restaurant" class="max-w-5xl mx-auto px-6 pt-12">

            <button @click="goBack"
                class="group flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-gray-400 hover:text-black transition-colors mb-12">
                <span class="group-hover:-translate-x-1 transition-transform">←</span>
                Volver
            </button>

            <header class="mb-16 border-b border-gray-100 pb-8">
                <h1 class="text-4xl md:text-6xl font-light tracking-tight text-black mb-4 leading-tight">
                    {{ restaurant.name }}
                </h1>

                <div class="flex items-center gap-6 font-mono text-sm text-gray-500">
                    <div class="flex items-center gap-2 text-black">
                        <span>★</span>
                        <span class="font-bold text-lg">
                            {{ restaurant.ratings?.mean ? restaurant.ratings.mean.toFixed(1) : 'N/A' }}
                        </span>
                    </div>

                    <span class="text-gray-200">/</span>

                    <span class="text-xs text-gray-400">ID: {{ route.params.id }}</span>
                </div>
            </header>

            <div v-if="restaurant.photos && restaurant.photos.length" class="space-y-1">
                <p class="text-xs font-mono uppercase tracking-widest text-gray-400 mb-4">Galería Visual</p>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1"> <a
                        v-for="(img, i) in restaurant.photos" :key="i" :href="img" target="_blank"
                        class="relative group overflow-hidden block aspect-square bg-gray-50"
                        :class="{ 'md:col-span-2 md:row-span-2': i === 0 }">
                        <img :src="img"
                            class="w-full h-full object-cover grayscale transition-all duration-700 ease-out group-hover:grayscale-0 group-hover:scale-105"
                            alt="Restaurant ambience" />

                        <div class="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-colors duration-300">
                        </div>
                    </a>
                </div>
            </div>

            <div v-else class="py-20 text-center border-t border-b border-gray-50">
                <p class="font-mono text-gray-300">No images available</p>
            </div>

        </div>
    </div>
</template>

<style scoped>
/* Sin estilos extra, todo con Tailwind */
</style>