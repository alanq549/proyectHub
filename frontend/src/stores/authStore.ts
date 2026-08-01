// src/stores/authStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService, type RegisterDTO, type LoginDTO } from '@/modules/auth/services/authService';

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<any | null>(JSON.parse(localStorage.getItem('user') || 'null'));

  const isAuthenticated = computed(() => !!token.value);

  async function register(data: RegisterDTO) {
    return await authService.register(data);
  }

  async function login(credentials: LoginDTO) {
    const response = await authService.login(credentials);
    
    // Guardar token y usuario
    token.value = response.token;
    user.value = response.user;
    
    localStorage.setItem('token', response.token);
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
    register,
    login,
    logout
  };
});