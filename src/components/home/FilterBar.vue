<template>
  <div class="filter-scroll">
    <div class="filter-bar">
      <button v-for="cat in categories" :key="cat" :class="{ active: modelValue === cat }"
        @click="$emit('update:modelValue', cat)">
        {{ formatCategory(cat) }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    required: true
  }
});

defineEmits(['update:modelValue']);

const categories = ['todos', 'restaurant', 'cafe', 'bar', 'fast_food', 'pub', 'bakery'];

const formatCategory = (cat) => {
  return cat === 'fast_food' ? 'Comida Rápida' : cat.charAt(0).toUpperCase() + cat.slice(1);
};
</script>

<style scoped>
.filter-scroll {
  position: absolute;
  top: 40px;
  left: 0;
  width: 100%;
  z-index: 999;
  overflow-x: auto;
  padding-bottom: 10px;
  -webkit-overflow-scrolling: touch;
}

.filter-bar {
  display: flex;
  gap: 10px;
  padding: 0 15px;
  width: max-content;
}

.filter-bar button {
  border: none;
  background: white;
  border-radius: 20px;
  padding: 8px 16px;
  font-weight: 600;
  font-size: 13px;
  color: #444;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.2s;
  cursor: pointer;
}

.filter-bar button.active {
  background: #222;
  color: white;
  transform: scale(1.05);
}
</style>
