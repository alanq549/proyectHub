<template>
  <div class="container-fluid p-4">
    <!-- Header de la Sección -->
    <div
      class="d-flex flex-column flex-md-row justify-content-between align-items-start align-items-md-center mb-4 gap-3"
    >
      <div>
        <h3 class="fw-bold mb-1 title-main">Gestión de Usuarios</h3>
        <p class="text-muted small mb-0">Control centralizado de identidades, roles y permisos del sistema.</p>
      </div>
      <button class="btn-app-primary d-flex align-items-center gap-2 px-3" @click="openCreateModal">
        <span class="material-symbols-outlined notranslate fs-5">person_add</span>
        <span>Nuevo Usuario</span>
      </button>
    </div>

    <!-- KPIs Rápidos con estilo Glassmorphism -->
    <div class="row g-3 mb-4">
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="app-card-glass p-3 d-flex align-items-center gap-3">
          <div class="kpi-icon-wrapper text-dark bg-slate-100">
            <span class="material-symbols-outlined notranslate fs-4">group</span>
          </div>
          <div>
            <div class="text-muted small fw-medium">Total Cuentas</div>
            <div class="fs-4 fw-bold text-dark">{{ userStore.users.length }}</div>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="app-card-glass p-3 d-flex align-items-center gap-3">
          <div class="kpi-icon-wrapper text-success bg-success-subtle">
            <span class="material-symbols-outlined notranslate fs-4">check_circle</span>
          </div>
          <div>
            <div class="text-muted small fw-medium">Usuarios Activos</div>
            <div class="fs-4 fw-bold text-dark">{{ userStore.activeUsersCount }}</div>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="app-card-glass p-3 d-flex align-items-center gap-3">
          <div class="kpi-icon-wrapper text-dark bg-slate-100">
            <span class="material-symbols-outlined notranslate fs-4">admin_panel_settings</span>
          </div>
          <div>
            <div class="text-muted small fw-medium">Administradores</div>
            <div class="fs-4 fw-bold text-dark">{{ userStore.adminUsersCount }}</div>
          </div>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="app-card-glass p-3 d-flex align-items-center gap-3">
          <div class="kpi-icon-wrapper text-danger bg-danger-subtle">
            <span class="material-symbols-outlined notranslate fs-4">block</span>
          </div>
          <div>
            <div class="text-muted small fw-medium">Cuentas Inactivas</div>
            <div class="fs-4 fw-bold text-dark">
              {{ userStore.users.length - userStore.activeUsersCount }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Contenedor Principal en Glassmorphism Table Card -->
    <div class="app-card-glass-table">
      <!-- Barra de Herramientas / Buscador -->
      <div class="p-3 border-bottom border-light-subtle bg-white bg-opacity-40">
        <div class="row g-2 align-items-center">
          <div class="col-12 col-md-6 col-lg-4">
            <div class="input-group app-input-group">
              <span class="input-group-text app-input-group-text">
                <span class="material-symbols-outlined notranslate fs-5">search</span>
              </span>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control app-input-control"
                placeholder="Buscar por usuario, nombre o email..."
              />
            </div>
          </div>
          <div class="col-6 col-md-3 col-lg-2">
            <select v-model="selectedRole" class="form-select custom-select">
              <option value="">Todos los Roles</option>
              <option value="admin">Administrador</option>
              <option value="user">Usuario Standard</option>
            </select>
          </div>
          <div class="col-6 col-md-3 col-lg-2">
            <select v-model="selectedStatus" class="form-select custom-select">
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
    </div>

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

<style scoped>
.title-main {
  color: var(--app-slate-900);
}

/* Botón Principal */
.btn-app-primary {
  background: var(--app-btn-primary-bg);
  color: #ffffff;
  border: none;
  height: var(--app-btn-primary-height);
  border-radius: var(--app-btn-radius-md);
  font-weight: 600;
  box-shadow: var(--app-btn-primary-shadow);
  transition: all 0.2s ease;
}

.btn-app-primary:hover {
  background: var(--app-btn-primary-bg-hover);
  transform: translateY(-1px);
}

/* Wrapper Iconos KPIs */
.kpi-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-slate-100 {
  background-color: var(--app-slate-100);
}

/* Selects personalizados */
.custom-select {
  border-color: var(--app-input-border);
  border-radius: var(--app-input-radius);
  font-size: 0.875rem;
}

.custom-select:focus {
  border-color: var(--app-input-focus-accent);
  box-shadow: var(--app-input-focus-ring);
}
</style>