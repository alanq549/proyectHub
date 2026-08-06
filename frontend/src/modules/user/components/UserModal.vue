<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4 animate-in fade-in duration-200">
    <div class="bg-white/90 backdrop-blur-md rounded-2xl max-w-2xl w-full shadow-2xl border border-white/60 overflow-hidden flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="p-5 border-b border-slate-100/80 flex items-center justify-between bg-white/40">
        <h5 class="text-lg font-semibold text-slate-800 flex items-center gap-2.5 m-0">
          <span class="material-symbols-outlined notranslate text-indigo-600 bg-indigo-50 p-2 rounded-xl text-xl">
            {{ isEditing ? 'manage_accounts' : 'person_add' }}
          </span>
          {{ isEditing ? 'Editar Usuario' : 'Nuevo Usuario' }}
        </h5>
        <button 
          type="button" 
          class="w-9 h-9 flex items-center justify-center rounded-xl text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition-colors" 
          @click="$emit('close')"
        >
          <span class="material-symbols-outlined notranslate text-xl">close</span>
        </button>
      </div>

      <!-- Body -->
      <div class="p-6 overflow-y-auto">
        <form @submit.prevent="handleSubmit" class="space-y-5">
         <!-- Subida de Avatar -->
<div class="flex items-center gap-4 p-4 bg-slate-50/70 border border-slate-100 rounded-2xl">
  <img 
    :src="avatarUrl" 
    alt="Preview Avatar" 
    class="w-16 h-16 rounded-full object-cover border-2 border-white shadow-sm ring-1 ring-slate-200"
  />
  <div class="flex-1 min-w-0">
    <label class="block font-medium text-xs text-slate-600 mb-1.5">Foto de Perfil</label>
    <input 
      type="file" 
      class="block w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-medium file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 file:transition-colors file:cursor-pointer cursor-pointer" 
      accept="image/*" 
      @change="handleFileChange"
    />
    <span class="block mt-1.5 text-[11px] text-slate-400">Formatos permitidos: JPG, PNG. Máx 2MB.</span>
  </div>
</div>

          <!-- Form Fields -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block font-medium text-xs text-slate-600 mb-1">Nombre(s)</label>
              <input 
                v-model="form.first_name" 
                type="text" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400 text-slate-700" 
                placeholder="Ej. Alan" 
              />
            </div>

            <div>
              <label class="block font-medium text-xs text-slate-600 mb-1">Apellido(s)</label>
              <input 
                v-model="form.last_name" 
                type="text" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400 text-slate-700" 
                placeholder="Ej. Arriaga" 
              />
            </div>

            <div>
              <label class="block font-medium text-xs text-slate-600 mb-1">Nombre de Usuario <span class="text-rose-500">*</span></label>
              <input 
                v-model="form.username" 
                type="text" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400 text-slate-700" 
                required 
                placeholder="Ej. alanq" 
              />
            </div>

            <div>
              <label class="block font-medium text-xs text-slate-600 mb-1">Correo Electrónico <span class="text-rose-500">*</span></label>
              <input 
                v-model="form.email" 
                type="email" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400 text-slate-700" 
                required 
                placeholder="usuario@correo.com" 
              />
            </div>

            <div v-if="!isEditing">
              <label class="block font-medium text-xs text-slate-600 mb-1">Contraseña <span class="text-rose-500">*</span></label>
              <input 
                v-model="form.password" 
                type="password" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all placeholder:text-slate-400 text-slate-700" 
                required 
                placeholder="••••••••" 
              />
            </div>

            <div>
              <label class="block font-medium text-xs text-slate-600 mb-1">Rol en el Sistema <span class="text-rose-500">*</span></label>
              <select 
                v-model="form.role" 
                class="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all text-slate-700 cursor-pointer" 
                required
              >
                <option value="user">Usuario Standard</option>
                <option value="admin">Administrador</option>
              </select>
            </div>

            <!-- Custom Tailwind Switch -->
            <div class="flex items-center pt-2">
              <label for="userActiveCheck" class="relative inline-flex items-center cursor-pointer select-none">
                <input 
                  v-model="form.is_active" 
                  type="checkbox" 
                  id="userActiveCheck" 
                  class="sr-only peer" 
                />
                <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none ring-offset-2 peer-focus:ring-2 peer-focus:ring-indigo-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
                <span class="ml-3 text-xs font-medium text-slate-700">Cuenta Activa</span>
              </label>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-3 mt-6 pt-4 border-t border-slate-100">
            <button 
              type="button" 
              class="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100/80 rounded-xl transition-colors bg-white border border-slate-200/80" 
              @click="$emit('close')"
            >
              Cancelar
            </button>
            <button 
              type="submit" 
              class="px-5 py-2 text-xs font-semibold text-white bg-slate-900 hover:bg-slate-800 rounded-xl transition-colors disabled:opacity-50 inline-flex items-center gap-2 shadow-sm" 
              :disabled="loading"
            >
              <span v-if="loading" class="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              <span>{{ isEditing ? 'Guardar Cambios' : 'Crear Usuario' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, watch, computed } from 'vue';
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