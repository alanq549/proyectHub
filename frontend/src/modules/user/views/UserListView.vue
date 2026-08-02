<template>
  <div class="container-fluid p-4">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="fw-bold mb-1">Gestión de Usuarios</h3>
        <p class="text-muted small mb-0">Administra los accesos y cuentas del sistema.</p>
      </div>
      <button class="btn btn-primary d-flex align-items-center gap-2" @click="openCreateModal">
        <span class="material-symbols-outlined fs-5">add</span>
        Nuevo Usuario
      </button>
    </div>

    <!-- Tabla -->
    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="bg-light">
              <tr>
                <th class="ps-4">ID</th>
                <th>Usuario</th>
                <th>Correo</th>
                <th class="text-end pe-4">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td class="ps-4 fw-semibold text-muted">#{{ user.id }}</td>
                <td class="fw-medium">{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td class="text-end pe-4">
                  <button class="btn btn-sm btn-outline-secondary me-2" @click="openEditModal(user)">
                    <span class="material-symbols-outlined fs-6">edit</span>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="deleteUser(user.id!)">
                    <span class="material-symbols-outlined fs-6">delete</span>
                  </button>
                </td>
              </tr>
              <tr v-if="users.length === 0">
                <td colspan="4" class="text-center py-4 text-muted">No hay usuarios registrados.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal Form -->
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
import { ref, onMounted } from 'vue';
import { userService, type User } from '../services/userService';
import UserModal from '../components/UserModal.vue';

const users = ref<User[]>([]);
const showModal = ref(false);
const selectedUser = ref<User | null>(null);
const saving = ref(false);

const loadUsers = async () => {
  try {
    users.value = await userService.getUsers();
  } catch (err) {
    console.error('Error al cargar usuarios:', err);
  }
};

const openCreateModal = () => {
  selectedUser.value = null;
  showModal.value = true;
};

const openEditModal = (user: User) => {
  selectedUser.value = user;
  showModal.value = true;
};

const handleSave = async (formData: any) => {
  saving.value = true;
  try {
    if (selectedUser.value?.id) {
      await userService.updateUser(selectedUser.value.id, formData);
    } else {
      await userService.createUser(formData);
    }
    showModal.value = false;
    await loadUsers();
  } catch (err) {
    alert('Error al guardar datos');
  } finally {
    saving.value = false;
  }
};

const deleteUser = async (id: number) => {
  if (confirm('¿Seguro de eliminar este usuario?')) {
    try {
      await userService.deleteUser(id);
      await loadUsers();
    } catch (err) {
      alert('Error al eliminar usuario');
    }
  }
};

onMounted(loadUsers);
</script>