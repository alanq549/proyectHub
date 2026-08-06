import type { RouteRecordRaw } from 'vue-router'

export const callsRoutes: RouteRecordRaw[] = [
  {
    path: '/calls',
    name: 'calls-list',
    component: () => import('../views/CallsListView.vue'),
    meta: { requiresAuth: true }
  }
]