import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './pages/HomePage.vue'
import auth_router from './features/auth/router'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    ...auth_router
  ],
})

export default router