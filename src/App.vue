<template>
  <div>

    <nav class="hidden md:flex bg-white shadow px-8 py-4 justify-between items-center sticky top-0 z-50">
      <div class=" text-gray-700 md:text-3xl font-light tracking-tighter">Concierge</div>

      <div class="flex gap-8">
        <router-link 
          to="/" 
          class="text-gray-600 hover:text-blue-600 font-medium transition-colors"
          active-class="text-blue-700 font-light border-b-2 border-blue-700"
        >
          Inicio
        </router-link>

        <router-link 
          to="/recommend" 
          class="text-gray-600 hover:text-blue-600 font-medium transition-colors"
          active-class="text-blue-700 font-light border-b-2 border-blue-700"
        >
          Recomendador
        </router-link>
      </div>
    </nav>

    <main class=" p-4">
      <router-view />
    </main>

    <nav class="md:hidden fixed bottom-0 left-0 w-full bg-white border-t border-gray-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] flex justify-around items-center py-3 z-50">
      
      <router-link 
        to="/" 
        class="flex flex-col items-center gap-1 text-xs text-gray-500 transition-colors"
        active-class="!text-blue-600 font-bold"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/> 
          <polyline points="9 22 9 12 15 12 15 22"/>
        </svg>
        <span>Inicio</span>
      </router-link>

      <router-link 
        to="/recommend" 
        class="flex flex-col items-center gap-1 text-xs text-gray-500 transition-colors"
        active-class="!text-blue-600 font-bold"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>
        </svg>
        <span>Recomendador</span>
      </router-link>

    </nav>

  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>