// src/modules/user/stores/userStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { userService, type User, type UserPayload } from '../services/userService';

export const USER_CACHE_KEY = 'projecthub.users.v1';

interface PersistedUsersCache {
  users: User[];
  isLoaded: true;
}

function readCachedUsers(): User[] | null {
  try {
    const cachedValue = localStorage.getItem(USER_CACHE_KEY);

    if (!cachedValue) return null;

    const cache = JSON.parse(cachedValue) as PersistedUsersCache;
    return cache.isLoaded && Array.isArray(cache.users) ? cache.users : null;
  } catch {
    return null;
  }
}

function persistUsers(users: User[]) {
  try {
    localStorage.setItem(USER_CACHE_KEY, JSON.stringify({ users, isLoaded: true }));
  } catch {
    // The in-memory cache remains available when browser storage is unavailable.
  }
}

export const useUserStore = defineStore('user', () => {
  const cachedUsers = readCachedUsers();
  const users = ref<User[]>(cachedUsers ?? []);
  const loading = ref(false);
  const isLoaded = ref(cachedUsers !== null);
  let activeRequest: Promise<void> | null = null;

  const activeUsersCount = computed(() => users.value.filter(u => u.is_active !== false).length);
  const adminUsersCount = computed(() => users.value.filter(u => u.role === 'admin').length);

  // Uses the persisted cache unless an explicit refresh is requested.
  function fetchUsers(forceRefresh = false): Promise<void> {
    if (activeRequest) return activeRequest;

    // Local storage is only a fast initial render. Revalidate on every view
    // entry so server-side seeds and changes from other sessions are reflected.
    loading.value = forceRefresh || !isLoaded.value;
    activeRequest = userService
      .getUsers()
      .then((receivedUsers) => {
        users.value = receivedUsers;
        isLoaded.value = true;
        persistUsers(receivedUsers);
      })
      .catch((err) => {
        console.error('Error al cargar usuarios:', err);
        throw err;
      })
      .finally(() => {
        loading.value = false;
        activeRequest = null;
      });

    return activeRequest;
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
      persistUsers(users.value);
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
