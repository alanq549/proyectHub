<template>
  <div class="tw-fixed tw-inset-0 tw-z-50 tw-flex tw-items-center tw-justify-center tw-bg-black/50 tw-backdrop-blur-sm tw-p-4">
    <AppCard variant="glass" padding="none" class="tw-max-w-2xl tw-w-full tw-max-h-[90vh] tw-flex tw-flex-col tw-overflow-hidden tw-border tw-border-outline-variant/60 tw-shadow-[0_8px_30px_rgba(0,0,0,0.35)]">
      <!-- Header -->
      <div class="tw-px-5 tw-py-4 tw-border-b tw-border-outline-variant tw-flex tw-items-center tw-justify-between tw-bg-surface-container-lowest/40">
        <h5 class="tw-text-lg tw-font-semibold tw-text-on-surface tw-flex tw-items-center tw-gap-2.5 tw-m-0">
          <span class="material-symbols-outlined notranslate tw-text-on-primary tw-bg-primary tw-p-2 tw-rounded-xl tw-text-xl">
            {{ isEditing ? 'manage_accounts' : 'person_add' }}
          </span>
          {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
        </h5>
        <button
          type="button"
          class="tw-w-9 tw-h-9 tw-flex tw-items-center tw-justify-center tw-rounded-xl tw-text-outline hover:tw-bg-surface-container hover:tw-text-on-surface tw-transition-colors"
          @click="$emit('close')"
        >
          <span class="material-symbols-outlined notranslate tw-text-xl">close</span>
        </button>
      </div>

      <!-- Body -->
      <div class="tw-p-6 tw-overflow-y-auto">
        <form @submit.prevent="handleSubmit" class="tw-space-y-5">
          <!-- Subida de Avatar -->
          <div class="tw-flex tw-items-center tw-gap-4 tw-p-4 tw-bg-surface-container-low/60 tw-border tw-border-dashed tw-border-primary/30 tw-rounded-2xl">
            <img
              :src="avatarUrl"
              alt="Preview Avatar"
              class="tw-w-16 tw-h-16 tw-rounded-full tw-object-cover tw-border-2 tw-border-outline-variant tw-shadow-sm"
            />
            <div class="tw-flex-1 tw-min-w-0">
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1.5 tw-flex tw-items-center tw-gap-1.5">
                <span class="material-symbols-outlined notranslate tw-text-sm tw-text-primary">image</span>
                Foto de Perfil
              </label>
              <input
                type="file"
                class="tw-block tw-w-full tw-text-xs tw-text-on-surface-variant file:tw-mr-3 file:tw-py-1.5 file:tw-px-3 file:tw-rounded-lg file:tw-border-0 file:tw-text-xs file:tw-font-medium file:tw-bg-primary/15 file:tw-text-primary hover:file:tw-bg-primary/25 file:tw-transition-colors file:tw-cursor-pointer tw-cursor-pointer"
                accept="image/*"
                @change="handleFileChange"
              />
              <span class="tw-block tw-mt-1.5 tw-text-[11px] tw-text-outline">Formatos permitidos: JPG, PNG. Máx 2MB.</span>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
            <div>
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Nombre(s)</label>
              <AppInput v-model="form.first_name" placeholder="Ej. Alan" />
            </div>

            <div>
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Apellido(s)</label>
              <AppInput v-model="form.last_name" placeholder="Ej. Arriaga" />
            </div>

            <div>
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Nombre de Usuario <span class="tw-text-primary">*</span></label>
              <AppInput v-model="form.username" icon="alternate_email" placeholder="Ej. alanq" />
            </div>

            <div>
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Correo Electrónico <span class="tw-text-primary">*</span></label>
              <AppInput v-model="form.email" type="email" icon="mail" placeholder="usuario@correo.com" />
            </div>

            <div v-if="!isEditing">
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Contraseña <span class="tw-text-primary">*</span></label>
              <AppInput v-model="form.password" type="password" icon="lock" placeholder="••••••••" />
            </div>

            <div>
              <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Rol en el Sistema <span class="tw-text-primary">*</span></label>
              <select
                v-model="form.role"
                required
                class="tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3.5 tw-py-2.5 tw-text-sm tw-text-on-surface focus:tw-border-primary focus:tw-outline-none focus:tw-ring-1 focus:tw-ring-primary tw-transition-all tw-cursor-pointer"
              >
                <option value="user">Usuario Standard</option>
                <option value="admin">Administrador</option>
              </select>
            </div>

            <!-- Switch Cuenta Activa -->
            <div class="tw-flex tw-items-center tw-pt-2">
              <label for="userActiveCheck" class="tw-relative tw-inline-flex tw-items-center tw-cursor-pointer tw-select-none">
                <input
                  v-model="form.is_active"
                  type="checkbox"
                  id="userActiveCheck"
                  class="tw-sr-only tw-peer"
                />
                <div class="tw-w-11 tw-h-6 tw-bg-surface-container-highest peer-focus:tw-outline-none peer-focus:tw-ring-2 peer-focus:tw-ring-primary/20 tw-rounded-full tw-peer peer-checked:after:tw-translate-x-full peer-checked:after:tw-border-white after:tw-content-[''] after:tw-absolute after:tw-top-[2px] after:tw-left-[2px] after:tw-bg-white after:tw-border-outline-variant after:tw-border after:tw-rounded-full after:tw-h-5 after:tw-w-5 after:tw-transition-all peer-checked:tw-bg-primary"></div>
                <span class="tw-ml-3 tw-text-xs tw-font-medium tw-text-on-surface-variant">Cuenta Activa</span>
              </label>
            </div>
          </div>

          <!-- Actions -->
          <div class="tw-flex tw-justify-end tw-gap-3 tw-mt-6 tw-pt-4 tw-border-t tw-border-outline-variant">
            <AppButton type="button" variant="secondary" @click="$emit('close')">Cancelar</AppButton>
            <AppButton type="submit" variant="primary" :loading="loading" icon="save">
              {{ isEditing ? 'Guardar Cambios' : 'Crear Usuario' }}
            </AppButton>
          </div>
        </form>
      </div>
    </AppCard>
  </div>
</template>


<script setup lang="ts">
import { ref, watch, computed } from 'vue';
import type { User } from '../services/userService';
import AppCard from '@/shared/components/AppCard.vue';
import AppButton from '@/shared/components/AppButton.vue';
import AppInput from '@/shared/components/AppInput.vue';

const props = defineProps<{
  userToEdit?: User | null;
  loading?: boolean;
}>();

const emit = defineEmits(['close', 'save']);

const isEditing = ref(false);
const defaultAvatar = import.meta.env.VITE_STATIC_URL + '/static/defaults/icon_default.png';
const previewAvatar = ref<string | null>(null);
const selectedFile = ref<File | null>(null);

// Computada para manejar los 3 casos (Blob local, ruta del backend o avatar por defecto)
const avatarUrl = computed(() => {
  if (!previewAvatar.value) {
    return defaultAvatar;
  }

  // Caso 1: Imagen local recién seleccionada (blob:http://...) o URL completa externa (https://...)
  if (previewAvatar.value.startsWith('blob:') || previewAvatar.value.startsWith('http')) {
    return previewAvatar.value;
  }

  // Caso 2: Ruta relativa recibida del backend (/static/uploads/...)
  const baseUrl = import.meta.env.VITE_STATIC_URL || '';
  const cleanPath = previewAvatar.value.startsWith('/') ? previewAvatar.value : `/${previewAvatar.value}`;
  return `${baseUrl}${cleanPath}`;
});

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
    // Genera un Blob temporal para la vista previa instantánea
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
  data.append('is_active', form.value.is_active ? 'true' : 'false');

  if (!isEditing.value && form.value.password) {
    data.append('password', form.value.password);
  }

  if (selectedFile.value) {
    data.append('file', selectedFile.value);
  }

  emit('save', data);
};
</script>
