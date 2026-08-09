import type { RouteRecordRaw } from 'vue-router'

export const historyRoutes: RouteRecordRaw[] = [
  {
    path: '/history',
    name: 'history',
    component: () => import('../views/HistoryView.vue'),
    meta: { requiresAuth: true }
  }
]