import { createRouter, createWebHistory } from 'vue-router'
import { authRoutes } from '@/modules/auth/routes'
import HomeView from '@/views/HomeView.vue'

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
    ...authRoutes

    // 3. Puedes ir sumando otros módulos aquí en el futuro:
    // dashboardRoutes,
    // projectsRoutes,

    // 4. Ruta para capturar 404 Not Found
    //{
    //  path: '/:pathMatch(.*)*',
    //  name: 'not-found',
    //  component: () => import('@/views/NotFoundView.vue')
    // }
  ]
})

// Opcional: Modificar el título del documento según las rutas
router.beforeEach((to, from) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} | ProjectHub`
  }
})

export default router