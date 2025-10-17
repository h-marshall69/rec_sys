<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Tus Recomendaciones</h1>
    
    <!-- Info del usuario -->
    <div class="bg-blue-50 p-4 rounded-lg mb-6">
      <p class="text-lg">Usuario ID: {{ userId }}</p>
      <p class="text-lg">Géneros seleccionados: {{ selectedGenres.join(', ') }}</p>
    </div>

    <!-- Lista de recomendaciones -->
    <div class="grid gap-4 md:grid-cols-2">
      <div v-for="movie in recommendations" :key="movie.movieId" 
           class="bg-white p-4 rounded-lg shadow-md border">
        <h3 class="text-xl font-semibold mb-2">{{ movie.title }}</h3>
        <p class="text-gray-600 mb-2">Géneros: {{ movie.genres }}</p>
        <div class="flex justify-between text-sm">
          <span class="bg-yellow-100 px-2 py-1 rounded">⭐ {{ movie.avg_rating }}</span>
          <span class="bg-gray-100 px-2 py-1 rounded">👥 {{ movie.rating_count }}</span>
        </div>
      </div>
    </div>

    <div v-if="recommendations.length === 0" class="text-center py-8">
      <p class="text-gray-500">No hay recomendaciones disponibles.</p>
    </div>
  </div>
</template>

<script setup>
import { useRecommendationsStore } from '../store/recommendations'
import { ref, onMounted } from 'vue'

const recommendations = ref([])
const userId = ref('')
const selectedGenres = ref([])

const store = useRecommendationsStore()
recommendations.value = store.recommendations
userId.value = store.userId
selectedGenres.value = store.selectedGenres
</script>



<style scoped></style>