<!-- src\views\Recommend.vue -->
<script setup>
import RecommendBox from "../components/RecommendBox.vue";
</script>

<template>
  <div class="bg-white text-gray-900 font-sans relative  flex flex-col md:justify-center">

    <div class="w-full max-w-2xlmx-auto px-4 md:px-0">

      <div class="text-center mb-8 md:mb-12">
        <h1 class="text-3xl md:text-5xl font-light tracking-tighter mb-2">
          Concierge AI
        </h1>
        <p class="text-[10px] md:text-xs font-mono uppercase tracking-[0.2em] text-gray-400">
          Descubre Puno a tu medida
        </p>
        
      </div>

      <div class="w-full">
        <RecommendBox />
      </div>

    </div>
  </div>
</template>