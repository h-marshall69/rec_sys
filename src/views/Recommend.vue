<!-- src\views\Recommend.vue -->
<script setup>
import RecommendBox from "../components/RecommendBox.vue";
</script>

<template>
    <div class="min-h-screen bg-white text-gray-900 font-sans relative">

        <nav class="absolute top-8 left-8 md:top-12 md:left-12">
            <router-link to="/"
                class="group flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-gray-300 hover:text-black transition-colors">
                <span class="group-hover:-translate-x-1 transition-transform">←</span>
                Home
            </router-link>
        </nav>

        <div class="max-w-2xl mx-auto px-6 pt-32 md:pt-40 pb-20">

            <div class="text-center mb-16">
                <h1 class="text-3xl md:text-4xl font-light tracking-tighter mb-2">
                    Concierge AI
                </h1>
                <p class="text-[10px] font-mono uppercase tracking-[0.2em] text-gray-400">
                    Descubre Puno a tu medida
                </p>
            </div>

            <RecommendBox />

        </div>
    </div>
</template>