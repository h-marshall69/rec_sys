<!-- src\components\SearchBox.vue - Versión mejorada -->
<script setup>
import { ref, watch } from "vue";
import api from "../services/api";

const query = ref("");
const results = ref([]);
const loading = ref(false);
const showResults = ref(false);

let timeout = null;

watch(query, (val) => {
  clearTimeout(timeout);
  if (!val || val.length < 2) {
    results.value = [];
    showResults.value = false;
    return;
  }

  timeout = setTimeout(async () => {
    loading.value = true;
    try {
      const { data } = await api.get("/search", {
        params: { q: val }
      });
      results.value = data;
      showResults.value = true;
    } catch (e) {
      console.error(e);
    } finally {
      loading.value = false;
    }
  }, 400);
});

const closeResults = () => {
  setTimeout(() => {
    showResults.value = false;
  }, 200);
};
</script>

<template>
  <div class="relative">
    <div class="relative">
      <input
        v-model="query"
        @focus="showResults = results.length > 0"
        @blur="closeResults"
        placeholder="Buscar restaurante por nombre..."
        class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-300 focus:border-transparent transition-all"
      />
      
      <!-- Icono de búsqueda -->
      <div class="absolute right-3 top-3 text-gray-400">
        <svg v-if="loading" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
      </div>
    </div>

    <!-- Resultados de búsqueda -->
    <div 
      v-if="showResults && results.length"
      class="absolute z-50 bg-white w-full mt-2 rounded-lg shadow-lg border border-gray-100 max-h-96 overflow-y-auto"
    >
      <div class="p-2">
        <div v-for="r in results" :key="r.locationId" class="mb-1 last:mb-0">
          <router-link
            :to="`/restaurants/${r.locationId}`"
            class="flex items-center justify-between px-4 py-3 hover:bg-gray-50 rounded-lg transition-colors"
          >
            <div class="flex-1">
              <p class="font-medium text-gray-900">{{ r.localizedName }}</p>
              <p v-if="r.address" class="text-sm text-gray-500 truncate">{{ r.address }}</p>
            </div>
            <div class="flex items-center ml-4">
              <span class="text-amber-500 font-medium">★ {{ r.rating_mean?.toFixed(1) || 'N/A' }}</span>
            </div>
          </router-link>
        </div>
      </div>
      
      <div class="border-t border-gray-100 px-4 py-2 bg-gray-50 rounded-b-lg">
        <p class="text-xs text-gray-500">{{ results.length }} resultado{{ results.length !== 1 ? 's' : '' }} encontrado{{ results.length !== 1 ? 's' : '' }}</p>
      </div>
    </div>
  </div>
</template>