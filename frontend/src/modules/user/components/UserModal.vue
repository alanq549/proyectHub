<template>
  <div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content rounded-4 border-0 shadow">
        <div class="modal-header border-bottom px-4 py-3">
          <h5 class="modal-title fw-bold text-dark d-flex align-items-center gap-2">
            <span class="material-symbols-outlined notranslate text-primary">
              {{ isEditing ? 'manage_accounts' : 'person_add' }}
            </span>
            {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <div class="modal-body p-4">
          <form @submit.prevent="handleSubmit">
            <!-- Selección de Avatar / Foto -->
            <div class="d-flex align-items-center gap-3 mb-4 p-3 bg-light rounded-3">
              <img 
                :src="previewAvatar || defaultAvatar" 
                alt="Preview Avatar" 
                class="rounded-circle object-fit-cover border"
                width="64" 
                height="64"
              />
              <div class="flex-grow-1">
                <label class="form-label text-secondary small fw-medium mb-1">Foto de Perfil</label>
                <input 
                  type="file" 
                  class="form-control form-control-sm" 
                  accept="image/*" 
                  @change="handleFileChange"
                />
                <span class="form-text text-muted small">Formatos permitidos: JPG, PNG. Máx 2MB.</span>
              </div>
            </div>

            <div class="row g-3">
              <!-- Nombre y Apellidos -->
              <div class="col-12 col-md-6">
                <label class="form-label text-secondary small fw-medium">Nombre(s)</label>
                <input v-model="form.first_name" type="text" class="form-control" placeholder="Ej. Alan" />
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label text-secondary small fw-medium">Apellido(s)</label>
                <input v-model="form.last_name" type="text" class="form-control" placeholder="Ej. Arriaga" />
              </div>

              <!-- Username y Email -->
              <div class="col-12 col-md-6">
                <label class="form-label text-secondary small fw-medium">Nombre de Usuario *</label>
                <input v-model="form.username" type="text" class="form-control" required placeholder="Ej. alanq" />
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label text-secondary small fw-medium">Correo Electrónico *</label>
                <input v-model="form.email" type="email" class="form-control" required placeholder="usuario@correo.com" />
              </div>

              <!-- Password -->
              <div class="col-12 col-md-6" v-if="!isEditing">
                <label class="form-label text-secondary small fw-medium">Contraseña *</label>
                <input v-model="form.password" type="password" class="form-control" required placeholder="••••••••" />
              </div>

              <!-- Rol y Estado -->
              <div class="col-12 col-md-6">
                <label class="form-label text-secondary small fw-medium">Rol en el Sistema *</label>
                <select v-model="form.role" class="form-select" required>
                  <option value="user">Usuario Standard</option>
                  <option value="admin">Administrador</option>
                </select>
              </div>

              <div class="col-12 col-md-6 d-flex align-items-center">
                <div class="form-check form-switch mt-3">
                  <input 
                    v-model="form.is_active" 
                    class="form-check-input" 
                    type="checkbox" 
                    id="userActiveCheck" 
                  />
                  <label class="form-check-label fw-medium text-dark" for="userActiveCheck">
                    Cuenta Activa
                  </label>
                </div>
              </div>
            </div>

            <!-- Footer con Botones -->
            <div class="d-flex justify-content-end gap-2 mt-4 pt-3 border-top">
              <button type="button" class="btn btn-light px-4" @click="$emit('close')">Cancelar</button>
              <button type="submit" class="btn btn-primary px-4 d-flex align-items-center gap-2" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm" role="status"></span>
                <span>{{ isEditing ? 'Guardar Cambios' : 'Crear Usuario' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import type { User } from '../services/userService';

const props = defineProps<{
  userToEdit?: User | null;
  loading?: boolean;
}>();

const emit = defineEmits(['close', 'save']);

const isEditing = ref(false);
const defaultAvatar = import.meta.env.VITE_STATIC_URL + '/static/defaults/icon_default.png';
const previewAvatar = ref<string | null>(null);
const selectedFile = ref<File | null>(null);

const form = ref({
  first_name: '',
  last_name: '',
  username: '',
  email: '',
  password: '',
  role: 'user',
  is_active: true
});

watch(() => props.userToEdit, (val) => {
  if (val) {
    isEditing.value = true;
    form.value = {
      first_name: val.first_name || '',
      last_name: val.last_name || '',
      username: val.username || '',
      email: val.email || '',
      password: '',
      role: val.role || 'user',
      is_active: val.is_active !== false
    };
    previewAvatar.value = val.profile_picture_url || null;
  } else {
    isEditing.value = false;
    form.value = {
      first_name: '',
      last_name: '',
      username: '',
      email: '',
      password: '',
      role: 'user',
      is_active: true
    };
    previewAvatar.value = null;
  }
  selectedFile.value = null;
}, { immediate: true });

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    selectedFile.value = file;
    previewAvatar.value = URL.createObjectURL(file);
  }
};

const handleSubmit = () => {
  const data = new FormData();
  data.append('username', form.value.username);
  data.append('email', form.value.email);
  data.append('first_name', form.value.first_name);
  data.append('last_name', form.value.last_name);
  data.append('role', form.value.role);
  
  // Enviar 'true' / 'false' en minúsculas explícitas
  data.append('is_active', form.value.is_active ? 'true' : 'false');

  if (!isEditing.value && form.value.password) {
    data.append('password', form.value.password);
  }

  // Se adjunta el archivo correctamente con la key 'file' que espera Flask
  if (selectedFile.value) {
    data.append('file', selectedFile.value);
  }

  emit('save', data);
};
</script>