<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow px-6 py-4 flex gap-6">
      <router-link to="/">Inicio</router-link>
      <router-link to="/recommend">Recomendador</router-link>
    </nav>

    <router-view />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style></style>
