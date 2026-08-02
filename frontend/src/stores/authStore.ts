// src/stores/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService, type RegisterDTO, type LoginDTO } from '@/modules/auth/services/authService';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role: 'admin' | 'user';
  profile_picture_url?: string;
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<User | null>(JSON.parse(localStorage.getItem('user') || 'null'));

  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === 'admin');

  // 💡 CENTRALIZACIÓN DE LA URL DE LA IMAGEN DE PERFIL
  const avatarUrl = computed(() => {
    const staticBase = import.meta.env.VITE_STATIC_URL || '';
    const defaultAvatar = `${staticBase}/static/defaults/icon_default.png`;

    const picturePath = user.value?.profile_picture_url;

    if (!picturePath) {
      return defaultAvatar;
    }

    // Si ya es una URL completa (ej. subida a Amazon S3 o una URL externa de HTTPS)
    if (picturePath.startsWith('http://') || picturePath.startsWith('https://')) {
      return picturePath;
    }

    // Si es una ruta relativa local de Flask/servidor estático
    return `${staticBase}${picturePath}`;
  });

  async function register(data: RegisterDTO) {
    return await authService.register(data);
  }

  async function login(credentials: LoginDTO) {
    const response = await authService.login(credentials);
    
    const accessToken = response.access_token; 
    
    token.value = accessToken;
    user.value = response.user;
    
    localStorage.setItem('token', accessToken);
    localStorage.setItem('user', JSON.stringify(response.user));

    return response;
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  return {
    token,
    user,
    isAuthenticated,
    isAdmin,
    avatarUrl, // 👈 Exportamos la propiedad computada
    register,
    login,
    logout
  };
});