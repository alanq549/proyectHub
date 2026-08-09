// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

import HomeView from '@/views/HomeView.vue'
import AppLayout from '@/layouts/AppLayout.vue'

import { authRoutes } from '@/modules/auth/routes'
import { userRoutes } from '@/modules/user/routes'
import { dashboardRoutes } from '@/modules/dashboard/routes'
import { callsRoutes } from '@/modules/calls/routes'
import { projectRoutes } from '@/modules/projects/routes'
import { documentsRoutes } from '@/modules/documents/routes'
import { historyRoutes } from '@/modules/history/routes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    // Rutas Privadas / Protegidas (Envueltas en AppLayout)
    {
      path: '/',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        ...dashboardRoutes,
        ...userRoutes,
        ...callsRoutes,
        ...projectRoutes,
        ...documentsRoutes,
        ...historyRoutes,
      ]
    },

    ...authRoutes,

    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from) => {
  const authStore = useAuthStore()

  if (to.meta.title) {
    document.title = `${to.meta.title} | ProjectHub`
  }

  const isAuthRoute = to.name === 'login' || to.name === 'register'

  // Punto 3.7: Redirigir si intenta ir a Home ('/') estando autenticado
  if (to.name === 'home' && authStore.isAuthenticated) {
    return authStore.isAdmin ? { name: 'users-list' } : { name: 'dashboard' }
  }

  // A. Si intenta ir a Login o Register estando AUTENTICADO
  if (isAuthRoute && authStore.isAuthenticated) {
    return authStore.isAdmin ? { name: 'users-list' } : { name: 'dashboard' }
  }

  // B. Si intenta ir a una ruta privada sin estar autenticado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }

  // C. Si la ruta requiere ser Admin y es un usuario común
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return { name: 'dashboard' }
  }

  return true
})

export default router