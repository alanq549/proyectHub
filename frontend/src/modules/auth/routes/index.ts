import type { RouteRecordRaw } from 'vue-router'

export const authRoutes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/modules/auth/views/LoginView.vue'),
    meta: { title: 'Iniciar Sesión' }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/modules/auth/views/RegisterView.vue'),
    meta: { title: 'Crear Cuenta' }
  }
]