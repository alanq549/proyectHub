import { createRouter, createWebHistory } from 'vue-router'
import { authRoutes } from '@/modules/auth/routes'
import HomeView from '@/views/HomeView.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 1. Redirección por defecto en la raíz
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    // 2. Módulo de Autenticación
    ...authRoutes,

    // Ruta de ejemplo protegida
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/HomeView.vue'), // Usar HomeView temporalmente
      meta: { requiresAuth: true, title: 'Dashboard' }
    },

    // 3. Puedes ir sumando otros módulos aquí en el futuro:
    // dashboardRoutes,
    // projectsRoutes,

    // 4. Ruta para capturar 404 Not Found
    // {
    //  path: '/:pathMatch(.*)*',
    //  name: 'not-found',
    //  component: () => import('@/views/NotFoundView.vue')
    // }
  ]
})

// Opcional: Modificar el título del documento según las rutas
// Navigation Guard (Protección de rutas)
router.beforeEach((to, from) => {
  const authStore = useAuthStore()

  // Cambiar título de la ventana
  if (to.meta.title) {
    document.title = `${to.meta.title} | ProjectHub`
  }

  // Si intenta ir al login/register estando ya logueado
  if (to.path.startsWith('/auth') && authStore.isAuthenticated) {
    return { name: 'home' }
  }

  // Si la ruta requiere autenticación y el usuario no está autenticado
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }

  // Continuar la navegación
  return true
})

export default router