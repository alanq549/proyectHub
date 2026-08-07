<template>
  <div class="tw-py-2 tw-max-w-7xl tw-mx-auto tw-space-y-6">
    <!-- Header de la Sección -->
    <div class="tw-flex tw-flex-col md:tw-flex-row tw-justify-between tw-items-start md:tw-items-center tw-gap-4">
      <div>
        <h1 class="tw-text-2xl tw-font-bold tw-text-on-surface tw-tracking-tight">Gestión de Usuarios</h1>
        <p class="tw-text-on-surface-variant tw-text-xs tw-mt-1">Control centralizado de identidades, roles y permisos del sistema.</p>
      </div>
      <AppButton variant="primary" icon="person_add" @click="openCreateModal">
        Nuevo Usuario
      </AppButton>
    </div>

    <!-- KPIs Rápidos -->
    <div class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 xl:tw-grid-cols-4 tw-gap-3">
      <AppCard variant="glass" padding="sm" class="tw-flex tw-items-center tw-gap-3">
        <div class="tw-w-11 tw-h-11 tw-rounded-2xl tw-bg-surface-container tw-text-on-surface-variant tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-2xl">group</span>
        </div>
        <div>
          <div class="tw-text-on-surface-variant tw-text-xs tw-font-medium">Total Cuentas</div>
          <div class="tw-text-2xl tw-font-bold tw-text-on-surface">{{ userStore.users.length }}</div>
        </div>
      </AppCard>

      <AppCard variant="glass" padding="sm" class="tw-flex tw-items-center tw-gap-3">
        <div class="tw-w-11 tw-h-11 tw-rounded-2xl tw-bg-success-bg tw-text-success tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-2xl">check_circle</span>
        </div>
        <div>
          <div class="tw-text-on-surface-variant tw-text-xs tw-font-medium">Usuarios Activos</div>
          <div class="tw-text-2xl tw-font-bold tw-text-on-surface">{{ userStore.activeUsersCount }}</div>
        </div>
      </AppCard>

      <AppCard variant="glass" padding="sm" class="tw-flex tw-items-center tw-gap-3">
        <div class="tw-w-11 tw-h-11 tw-rounded-2xl tw-bg-surface-container tw-text-on-surface-variant tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-2xl">admin_panel_settings</span>
        </div>
        <div>
          <div class="tw-text-on-surface-variant tw-text-xs tw-font-medium">Administradores</div>
          <div class="tw-text-2xl tw-font-bold tw-text-on-surface">{{ userStore.adminUsersCount }}</div>
        </div>
      </AppCard>

      <AppCard variant="glass" padding="sm" class="tw-flex tw-items-center tw-gap-3">
        <div class="tw-w-11 tw-h-11 tw-rounded-2xl tw-bg-error-bg tw-text-error tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-2xl">block</span>
        </div>
        <div>
          <div class="tw-text-on-surface-variant tw-text-xs tw-font-medium">Cuentas Inactivas</div>
          <div class="tw-text-2xl tw-font-bold tw-text-on-surface">{{ userStore.users.length - userStore.activeUsersCount }}</div>
        </div>
      </AppCard>
    </div>

    <!-- Tabla y buscador -->
    <AppCard variant="glass" padding="none">
      <!-- Barra de Herramientas / Buscador -->
      <div class="tw-px-4 tw-py-3 tw-border-b tw-border-outline-variant">
        <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-12 tw-gap-3 tw-items-center">
          <div class="md:tw-col-span-5">
            <AppInput
              v-model="searchQuery"
              icon="search"
              placeholder="Buscar por usuario, nombre o email..."
            />
          </div>
          <div class="md:tw-col-span-3">
            <select
              v-model="selectedRole"
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2.5 tw-text-sm tw-text-on-surface focus:tw-border-primary focus:tw-outline-none focus:tw-ring-1 focus:tw-ring-primary"
            >
              <option value="">Todos los Roles</option>
              <option value="admin">Administrador</option>
              <option value="user">Usuario Standard</option>
            </select>
          </div>
          <div class="md:tw-col-span-3">
            <select
              v-model="selectedStatus"
              class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2.5 tw-text-sm tw-text-on-surface focus:tw-border-primary focus:tw-outline-none focus:tw-ring-1 focus:tw-ring-primary"
            >
              <option value="">Todos los Estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Tabla Separada -->
      <UserTable
        :users="filteredUsers"
        @edit="openEditModal"
        @delete="handleDeleteUser"
      />
    </AppCard>

    <!-- Modal Form Completo -->
    <UserModal
      v-if="showModal"
      :userToEdit="selectedUser"
      :loading="saving"
      @close="showModal = false"
      @save="handleSave"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useUserStore } from '../stores/userStore';
import type { User, UserPayload } from '../services/userService';
import UserTable from '../components/UserTable.vue';
import UserModal from '../components/UserModal.vue';
import AppCard from '@/shared/components/AppCard.vue';
import AppButton from '@/shared/components/AppButton.vue';
import AppInput from '@/shared/components/AppInput.vue';

const userStore = useUserStore();

const showModal = ref(false);
const selectedUser = ref<User | null>(null);
const saving = ref(false);

const searchQuery = ref('');
const selectedRole = ref('');
const selectedStatus = ref('');

const filteredUsers = computed(() => {
  return userStore.users.filter((u: User) => {
    const query = searchQuery.value.toLowerCase().trim();
    const fullName = `${u.first_name || ''} ${u.last_name || ''}`.toLowerCase();

    const matchesSearch =
      !query ||
      u.username.toLowerCase().includes(query) ||
      u.email.toLowerCase().includes(query) ||
      fullName.includes(query);

    const matchesRole = !selectedRole.value || u.role === selectedRole.value;

    const isActive = u.is_active !== false;
    const matchesStatus =
      !selectedStatus.value ||
      (selectedStatus.value === 'active' && isActive) ||
      (selectedStatus.value === 'inactive' && !isActive);

    return matchesSearch && matchesRole && matchesStatus;
  });
});

const openCreateModal = () => {
  selectedUser.value = null;
  showModal.value = true;
};

const openEditModal = (user: User) => {
  selectedUser.value = user;
  showModal.value = true;
};

const handleSave = async (formData: UserPayload | FormData) => {
  saving.value = true;
  try {
    if (selectedUser.value?.id) {
      await userStore.updateUser(selectedUser.value.id, formData as UserPayload);
    } else {
      await userStore.createUser(formData as UserPayload);
    }
    showModal.value = false;
  } catch (err) {
    alert('Error al guardar datos del usuario');
  } finally {
    saving.value = false;
  }
};

const handleDeleteUser = async (id: number) => {
  if (confirm('¿Seguro que deseas eliminar este usuario?')) {
    try {
      await userStore.deleteUser(id);
    } catch (err) {
      alert('Error al eliminar el usuario');
    }
  }
};

onMounted(() => {
  userStore.fetchUsers();
});
</script>