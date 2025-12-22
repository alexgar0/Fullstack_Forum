import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './pages/HomePage.vue'
import auth_router from './features/auth/router'
import { branch_router } from './features/branch/router'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    ...auth_router,
    ...branch_router
  ],
})

export default router