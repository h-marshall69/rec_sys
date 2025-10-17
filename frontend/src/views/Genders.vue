<template>
    <div class="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
        <!-- Label y input mejorado con v-model y validación visual -->
        <div class="mb-4">
            <label for="userId" class="block text-sm font-medium text-gray-700 mb-2">
                ID de Usuario (nuevo)
            </label>
            <input id="userId" type="number" v-model="userId" placeholder="Ingresa un ID numérico"
                class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                :class="{ 'border-red-500': !userId && submitted }" required />
            <p v-if="!userId && submitted" class="text-red-500 text-xs mt-1">
                El ID es requerido.
            </p>
        </div>

        <!-- Título para los géneros -->
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Selecciona tus géneros favoritos:</h3>

        <!-- Botones de géneros con hover y transiciones -->
        <div class="flex flex-wrap gap-2 mb-6">
            <button v-for="genre in genres" :key="genre" @click="toggleGenre(genre)" :class="[
                'px-4 py-2 rounded-full border-2 transition-all duration-200 font-medium',
                selectedGenres.includes(genre)
                    ? 'bg-blue-600 text-white border-blue-600 hover:bg-blue-700 shadow-md'
                    : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200 hover:border-gray-400'
            ]">
                {{ genre }}
            </button>
        </div>

        <!-- Botón submit con loading -->
        <button @click="sendRecommendation" :disabled="loading || !userId || genres.length === 0"
            class="w-full px-6 py-3 bg-green-600 text-white rounded-md font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500">
            <span v-if="loading" class="flex items-center justify-center">
                <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                    viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                    </path>
                </svg>
                Buscando recomendaciones...
            </span>
            <span v-else>Enviar selección</span>
        </button>

        <!-- Mensaje de éxito/error más elegante -->
        <div v-if="message" :class="[
            'mt-4 p-3 rounded-md text-center font-medium',
            success ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
            {{ message }}
        </div>
    </div>
</template>

<script setup>
import api from '../services/axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRecommendationsStore } from '../store/recommendations'

const genres = ref([])
const selectedGenres = ref([])
const userId = ref("")
const loading = ref(false)
const submitted = ref(false)
const message = ref("")
const success = ref(false)

const responseData = ref(null)
const router = useRouter()
const recommendationsStore = useRecommendationsStore()

onMounted(async () => {
    try {
        const response = await api.get('/genres')
        genres.value = response.data.genres
    } catch (error) {
        console.error('Error al cargar géneros:', error)
        message.value = 'Error al cargar géneros. Intenta recargar la página.'
        success.value = false
    }
})

const toggleGenre = (genre) => {
    if (selectedGenres.value.includes(genre)) {
        selectedGenres.value = selectedGenres.value.filter(g => g !== genre)
    } else {
        selectedGenres.value.push(genre)
    }
}

const sendRecommendation = async () => {
    submitted.value = true
    if (!userId.value) {
        message.value = 'Por favor, ingresa un ID de usuario.'
        success.value = false
        return
    }

    try {
        loading.value = true
        message.value = ""
        const payload = {
            user_id: userId.value,
            selected_genres: selectedGenres.value,
        }
        // const response = await api.post('/users', payload)
        const response = await api.post('/recommendations', payload)
        responseData.value = response.data

        recommendationsStore.setRecommendations(response.data)

        message.value = '¡Preferencias enviadas con éxito!'
        success.value = true

        await router.push('/recommendations')
    } catch (error) {
        console.error('Error al enviar géneros:', error)
        message.value = 'Error al enviar. Verifica tu conexión e intenta de nuevo.'
        success.value = false
    } finally {
        loading.value = false
        // await router.push('/recommendations')
    }
}
</script>

<style scoped>
.max-w-md {
    max-width: 28rem;
}
</style>