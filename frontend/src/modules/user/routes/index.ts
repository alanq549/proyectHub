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
  }
]