<!-- src\views\RestaurantDetail.vue -->
<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const restaurant = ref(null);
const loading = ref(true);
const photos = ref([]);
const reviews = ref([]);
const reviewsError = ref(false);
const showingAllPhotos = ref(false);

onMounted(async () => {
    try {
        const { data } = await api.get(`/restaurants/${route.params.id}`);
        restaurant.value = data;
    } catch (e) {
        console.error(e);
    } finally {
        loading.value = false;
    }

    await loadReviews();
    await loadInitialPhotos();
});

const loadInitialPhotos = async () => {
    try {
        const { data } = await api.get(`/restaurants/${route.params.id}/photos`, {
            params: { limit: 4 }
        });
        photos.value = data;
    } catch (e) {
        console.error(e);
    }
};

const loadAllPhotos = async () => {
    try {
        const { data } = await api.get(`/restaurants/${route.params.id}/photos`);
        photos.value = data;
        showingAllPhotos.value = true;
    } catch (e) {
        console.error(e);
    }
};

const loadReviews = async () => {
    try {
        const { data } = await api.get(
            `/restaurants/${route.params.id}/reviews`,
            { params: { limit: 5 } }
        );
        reviews.value = data;
    } catch {
        reviewsError.value = true;
    }
};

const loadMoreReviews = async () => {
    try {
        const { data } = await api.get(
            `/restaurants/${route.params.id}/reviews`,
            { params: { limit: 10, offset: reviews.value.length } }
        );
        reviews.value = [...reviews.value, ...data];
    } catch {
        console.error("Error cargando más reseñas");
    }
};

const goBack = () => router.back();

// Función para crear array de estrellas (1-5)
const starArray = Array.from({ length: 5 }, (_, i) => i + 1);

// Función para calcular porcentaje de cada estrella
const calculateStarDistribution = () => {
    if (!restaurant.value?.ratings?.distribution) return Array(5).fill(0);

    const dist = restaurant.value.ratings.distribution;
    const total = Object.values(dist).reduce((sum, val) => sum + val, 0);

    return starArray.map(star => {
        const count = dist[star] || 0;
        return total > 0 ? (count / total) * 100 : 0;
    });
};
</script>

<template>
    <div class="min-h-screen bg-white text-gray-900">
        <!-- Header móvil sticky -->
        <div class="sticky top-0 bg-white z-10 border-b border-gray-100 px-4 py-3 md:hidden">
            <button @click="goBack" class="flex items-center gap-2 text-sm text-gray-600 hover:text-black">
                <span class="text-lg">←</span>
                <span>Volver</span>
            </button>
        </div>

        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 md:py-8">
            <!-- Botón volver desktop -->
            <button @click="goBack"
                class="hidden md:flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-gray-400 hover:text-black mb-8">
                <span>←</span>
                Volver
            </button>

            <!-- Loading State -->
            <div v-if="loading" class="animate-pulse space-y-8 pt-4">
                <div class="h-4 bg-gray-100 w-24 mb-6 rounded"></div>
                <div class="h-8 sm:h-12 bg-gray-100 w-3/4 rounded"></div>
                <div class="h-5 bg-gray-100 w-32 rounded"></div>
                <div class="grid grid-cols-2 gap-3 mt-6">
                    <div class="h-32 sm:h-40 bg-gray-100 rounded-lg"></div>
                    <div class="h-32 sm:h-40 bg-gray-100 rounded-lg"></div>
                </div>
            </div>

            <div v-else-if="restaurant">
                <!-- Header del restaurante -->
                <header class="border-b border-gray-100 pb-6 mb-8 md:pb-10 md:mb-12">
                    <h1 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-medium text-black mb-4">
                        {{ restaurant.name }}
                    </h1>

                    <!-- Rating principal -->
                    <div class="flex items-center gap-4 mb-4">
                        <div class="flex items-center gap-2">
                            <div class="flex items-center bg-amber-50 px-3 py-1.5 rounded-full">
                                <span class="text-amber-500 text-lg mr-1">★</span>
                                <span class="font-bold text-xl">
                                    {{ restaurant.ratings?.mean ? restaurant.ratings.mean.toFixed(1) : '0.0' }}
                                </span>
                                <span class="text-gray-500 text-sm ml-1">/5.0</span>
                            </div>
                            <span class="text-gray-500 text-sm">
                                {{ restaurant.ratings?.count || 0 }} reseña{{ restaurant.ratings?.count !== 1 ? 's' : ''
                                }}
                            </span>
                        </div>
                    </div>

                    <!-- Dirección -->
                    <div v-if="restaurant.address" class="flex items-start gap-2 text-gray-600">
                        <span class="text-gray-400 mt-0.5">📍</span>
                        <span class="text-sm">{{ restaurant.address }}</span>
                    </div>
                </header>

                <!-- Distribución de estrellas -->
                <section v-if="restaurant.ratings?.distribution" class="mb-8 p-4 bg-gray-50 rounded-lg">
                    <h3 class="text-sm font-medium text-gray-900 mb-3">Distribución de puntuaciones</h3>
                    <div class="space-y-2">
                        <div v-for="(percentage, index) in calculateStarDistribution()" :key="5 - index"
                            class="flex items-center">
                            <span class="text-sm text-gray-600 w-8">{{ 5 - index }} ★</span>
                            <div class="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden ml-2">
                                <div class="h-full bg-amber-500 rounded-full" :style="{ width: percentage + '%' }">
                                </div>
                            </div>
                            <span class="text-xs text-gray-500 ml-2 w-8">{{ percentage.toFixed(0) }}%</span>
                        </div>
                    </div>
                </section>

                <!-- Sección de Fotos -->
                <section class="mb-10 md:mb-16">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-sm font-medium text-gray-900">Fotos</h2>
                        <span class="text-xs text-gray-500">
                            {{ photos.length }} foto{{ photos.length !== 1 ? 's' : '' }}
                        </span>
                    </div>

                    <div v-if="photos.length === 0" class="py-8 text-center border border-gray-200 rounded-lg">
                        <p class="text-gray-400">No hay imágenes disponibles</p>
                    </div>

                    <!-- Galería de fotos -->
                    <div class="relative">
                        <div
                            class="flex md:grid md:grid-cols-2 lg:grid-cols-3 gap-3 overflow-x-auto md:overflow-visible pb-4 md:pb-0 scrollbar-hide">
                            <a v-for="(img, i) in photos" :key="i" :href="img" target="_blank"
                                class="flex-shrink-0 md:flex-shrink relative overflow-hidden block w-48 h-48 md:w-auto md:h-auto md:aspect-square bg-gray-100 rounded-lg"
                                :class="{ 'md:col-span-2 md:row-span-2': i === 0 && !showingAllPhotos }">
                                <img :src="img"
                                    class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                                    :alt="`Foto ${i + 1} de ${restaurant.name}`" loading="lazy" />
                            </a>
                        </div>

                        <!-- Indicador de scroll en móvil -->
                        <div v-if="photos.length > 2" class="md:hidden flex justify-center mt-2">
                            <div class="flex gap-1">
                                <div v-for="n in Math.min(3, photos.length)" :key="n"
                                    class="w-1.5 h-1.5 rounded-full bg-gray-300"></div>
                            </div>
                        </div>
                    </div>

                    <button v-if="!showingAllPhotos && photos.length >= 4" @click="loadAllPhotos"
                        class="mt-4 w-full md:w-auto py-2.5 px-4 text-sm font-medium text-gray-700 hover:text-black hover:bg-gray-50 border border-gray-300 rounded-lg flex items-center justify-center gap-2">
                        <span class="text-lg">+</span>
                        Ver todas las fotos
                    </button>
                </section>

                <!-- Sección de Reseñas -->
                <section class="border-t border-gray-100 pt-8 md:pt-12">
                    <div class="flex items-center justify-between mb-6">
                        <h2 class="text-sm font-medium text-gray-900">Reseñas de Clientes</h2>
                        <div class="flex items-center gap-1 bg-amber-50 px-3 py-1.5 rounded-full">
                            <span class="text-amber-500">★</span>
                            <span class="font-bold">{{ restaurant.ratings?.mean ? restaurant.ratings.mean.toFixed(1) :
                                '0.0' }}</span>
                            <span class="text-sm text-gray-500">/5.0</span>
                        </div>
                    </div>

                    <!-- Estados de error y vacío -->
                    <div v-if="reviewsError" class="py-8 text-center border border-gray-200 rounded-lg">
                        <p class="text-gray-400">Error cargando reseñas</p>
                        <p class="text-xs text-gray-500 mt-1">Intenta más tarde</p>
                    </div>

                    <div v-else-if="reviews.length === 0" class="py-8 text-center border border-gray-200 rounded-lg">
                        <p class="text-gray-400">Sin reseñas aún</p>
                        <p class="text-xs text-gray-500 mt-1">Sé el primero en opinar</p>
                    </div>

                    <!-- Lista de reseñas -->
                    <div v-else class="space-y-6">
                        <!-- Reseña destacada -->
                        <div v-if="reviews[0]"
                            class="border border-amber-100 rounded-xl p-5 bg-gradient-to-r from-amber-50 to-white">
                            <div class="flex items-start justify-between mb-3">
                                <div class="flex items-center gap-3">
                                    <div class="flex">
                                        <span v-for="star in starArray" :key="star" class="text-lg"
                                            :class="star <= reviews[0].rating ? 'text-amber-500' : 'text-gray-300'">
                                            ★
                                        </span>
                                    </div>
                                    <div class="flex items-center bg-white px-2 py-1 rounded-full">
                                        <span class="font-bold text-gray-900 text-sm">
                                            {{ reviews[0].rating.toFixed(1) }}
                                        </span>
                                        <span class="text-gray-400 text-xs ml-1">/5.0</span>
                                    </div>
                                </div>
                                <span class="text-xs text-gray-500 font-medium">{{ reviews[0].date }}</span>
                            </div>

                            <p class="text-gray-700 text-sm md:text-base mb-3">
                                {{ reviews[0].text }}
                            </p>

                            <div v-if="reviews[0].user" class="flex items-center gap-2">
                                <div class="w-7 h-7 bg-gradient-to-br from-amber-200 to-amber-300 rounded-full"></div>
                                <span class="text-sm text-gray-600 font-medium">{{ reviews[0].user }}</span>
                            </div>
                        </div>

                        <!-- Resto de reseñas -->
                        <div class="space-y-4">
                            <div v-for="(review, index) in reviews.slice(1)" :key="index"
                                class="border border-gray-100 rounded-lg p-4 hover:border-gray-200">
                                <div class="flex items-start justify-between mb-2">
                                    <div class="flex items-center gap-3">
                                        <div class="flex">
                                            <span v-for="star in starArray" :key="star" class="text-sm"
                                                :class="star <= review.rating ? 'text-amber-500' : 'text-gray-300'">
                                                ★
                                            </span>
                                        </div>
                                        <span class="font-bold text-gray-900 text-sm">
                                            {{ review.rating.toFixed(1) }}/5.0
                                        </span>
                                    </div>
                                    <span class="text-xs text-gray-500">{{ review.date }}</span>
                                </div>

                                <p class="text-gray-600 text-sm mb-3">
                                    {{ review.text }}
                                </p>

                                <div v-if="review.user" class="flex items-center gap-2">
                                    <span class="text-xs text-gray-500">{{ review.user }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- Botón cargar más reseñas -->
                        <button v-if="restaurant.ratings?.count > reviews.length" @click="loadMoreReviews"
                            class="w-full py-3 text-sm font-medium text-gray-700 hover:text-black hover:bg-gray-50 border border-gray-300 rounded-lg">
                            Ver más reseñas ({{ restaurant.ratings?.count - reviews.length }})
                        </button>
                    </div>
                </section>

                <!-- Información adicional -->
                <section v-if="restaurant.description || restaurant.hours"
                    class="mt-10 md:mt-16 pt-8 md:pt-12 border-t border-gray-100">
                    <h2 class="text-sm font-medium text-gray-900 mb-4 md:mb-6">Información adicional</h2>

                    <div class="space-y-6 md:space-y-0 md:grid md:grid-cols-1 lg:grid-cols-2 md:gap-8">
                        <div v-if="restaurant.description" class="space-y-2">
                            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wider">Descripción</h3>
                            <p class="text-gray-600 text-sm">{{ restaurant.description }}</p>
                        </div>

                        <div v-if="restaurant.hours" class="space-y-2">
                            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wider">Horarios</h3>
                            <div class="text-gray-600 text-sm bg-gray-50 p-4 rounded-lg">
                                {{ restaurant.hours }}
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    </div>
</template>

<style>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>