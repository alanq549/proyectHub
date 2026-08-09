import type { RouteRecordRaw } from 'vue-router'

 export const projectRoutes: RouteRecordRaw[] = [
  {
    path: '/projects',
    name: 'projects-list',
    component: () => import('../views/ProjectsListView.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/projects/:id',
    name: 'project-detail',
    component: () => import('../views/ProjectDetailView.vue'),
    meta: {
      requiresAuth: true
    }
  }
]

