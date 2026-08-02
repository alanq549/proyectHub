// src/modules/dashboard/routes/index.ts
import type { RouteRecordRaw } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'

export const dashboardRoutes: RouteRecordRaw[] = [
  {
    path: 'dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: { title: 'Panel Principal' }
  }
]