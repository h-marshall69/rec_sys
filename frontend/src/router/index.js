import { createRouter, createWebHistory } from 'vue-router'

import Genders from '../views/Genders.vue'
import Recommendations from '../views/Recommendations.vue'

const routes = [
  {
    path: '/',
    name: 'Genders',
    component: Genders
  },
  {
    path: '/recommendations',
    name: 'Recommendations',
    component: Recommendations
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router