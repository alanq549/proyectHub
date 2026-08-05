// src/modules/user/stores/userStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { userService, type User, type UserPayload } from '../services/userService';

export const useUserStore = defineStore('user', () => {
  const users = ref<User[]>([]);
  const loading = ref(false);
  const isLoaded = ref(false); // Flag para controlar la cache

  const activeUsersCount = computed(() => users.value.filter(u => u.is_active !== false).length);
  const adminUsersCount = computed(() => users.value.filter(u => u.role === 'admin').length);

  // Carga usuarios solo si no se han cargado previamente o si se fuerza el refresco
  async function fetchUsers(forceRefresh = false) {
    if (isLoaded.value && !forceRefresh) return;
    
    loading.value = true;
    try {
      users.value = await userService.getUsers();
      isLoaded.value = true;
    } catch (err) {
      console.error('Error al cargar usuarios:', err);
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createUser(payload: UserPayload) {
    loading.value = true;
    try {
      await userService.createUser(payload);
      await fetchUsers(true); // Invalida cache y refresca lista
    } finally {
      loading.value = false;
    }
  }

  async function updateUser(id: number, payload: UserPayload) {
    loading.value = true;
    try {
      await userService.updateUser(id, payload);
      await fetchUsers(true); // Invalida cache y refresca lista
    } finally {
      loading.value = false;
    }
  }

  async function deleteUser(id: number) {
    loading.value = true;
    try {
      await userService.deleteUser(id);
      users.value = users.value.filter(u => u.id !== id);
    } finally {
      loading.value = false;
    }
  }

  return {
    users,
    loading,
    isLoaded,
    activeUsersCount,
    adminUsersCount,
    fetchUsers,
    createUser,
    updateUser,
    deleteUser
  };
});