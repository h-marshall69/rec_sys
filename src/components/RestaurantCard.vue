<!-- src\components\RestaurantCard.vue -->
<script setup>
defineProps({
    restaurant: Object,
});
</script>

<template>
    <router-link :to="`/restaurants/${restaurant.locationId}`" class="group block h-full flex flex-col justify-between">
        <div>
            <span class="text-xs text-gray-300 font-mono mb-2 block group-hover:text-gray-500 transition-colors">
                #{{ restaurant.locationId }}
            </span>

            <h2
                class="text-2xl font-medium leading-tight text-gray-900 group-hover:text-black transition-colors mb-4 decoration-1 decoration-gray-300 underline-offset-4 group-hover:underline">
                {{ restaurant.localizedName }}
            </h2>
        </div>

        <div class="flex items-center justify-between border-t border-gray-100 pt-3 mt-2">

            <div class="flex items-center gap-2">
                <span class="text-sm font-bold">
                    ★ {{ restaurant.rating_mean ? restaurant.rating_mean.toFixed(1) : '-' }}
                </span>
            </div>

            <div class="text-xs font-mono text-gray-400">
                {{ restaurant.total_reviews_platform }} reseñas
            </div>
        </div>
    </router-link>
</template>