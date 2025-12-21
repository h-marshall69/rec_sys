import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import RestaurantDetail from '../views/RestaurantDetail.vue'
import Recommend from '../views/Recommend.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/restaurants/:id',
      name: 'restaurant-detail',
      component: RestaurantDetail,
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: Recommend,
    },
  ],
})

export default router
