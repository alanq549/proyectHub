<template>
  <div class="modal fade show d-block" tabindex="-1" style="background: rgba(0,0,0,0.5)">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content rounded-4 border-0 shadow">
        <div class="modal-header border-bottom-0 pb-0">
          <h5 class="modal-title fw-bold">
            {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
          </h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label text-secondary small fw-medium">Nombre de Usuario</label>
              <input v-model="form.username" type="text" class="form-control" required placeholder="ej. alanq" />
            </div>

            <div class="mb-3">
              <label class="form-label text-secondary small fw-medium">Correo Electrónico</label>
              <input v-model="form.email" type="email" class="form-control" required placeholder="usuario@correo.com" />
            </div>

            <div v-if="!isEditing" class="mb-3">
              <label class="form-label text-secondary small fw-medium">Contraseña</label>
              <input v-model="form.password" type="password" class="form-control" required placeholder="••••••••" />
            </div>

            <div class="d-flex justify-content-end gap-2 mt-4">
              <button type="button" class="btn btn-light" @click="$emit('close')">Cancelar</button>
              <button type="submit" class="btn btn-primary px-4" :disabled="loading">
                {{ isEditing ? 'Guardar Cambios' : 'Crear' }}
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
const form = ref({
  username: '',
  email: '',
  password: ''
});

watch(() => props.userToEdit, (val) => {
  if (val) {
    isEditing.value = true;
    form.value = { username: val.username, email: val.email, password: '' };
  } else {
    isEditing.value = false;
    form.value = { username: '', email: '', password: '' };
  }
}, { immediate: true });

const handleSubmit = () => {
  emit('save', { ...form.value });
};
</script>