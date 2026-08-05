/// src/modules/user/routes/index.ts
import UserListView from '../views/UserListView.vue'

export const userRoutes = [
  {
    path: '/users',
    name: 'users-list',
    component: UserListView,
    meta: { 
      requiresAuth: true, 
      requiresAdmin: true, 
      title: 'Gestión de Usuarios' 
    }
  },
  {
    path: '/profile', // 👈 Agregado el slash '/'
    name: 'user-profile',
    component: () => import('../views/ProfileView.vue'),
    meta: {
      title: 'Mi Perfil',
      requiresAuth: true
    }
  }
]