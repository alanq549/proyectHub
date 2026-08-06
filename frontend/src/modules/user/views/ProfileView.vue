<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { userService } from '../services/userService';
import UserAvatar from '@/layouts/components/UserAvatar.vue';

const authStore = useAuthStore();

const profileForm = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: ''
});

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
});

const selectedFile = ref<File | null>(null);
const previewUrl = ref<string | null>(null);

const profileMessage = ref({ type: '', text: '' });
const passwordMessage = ref({ type: '', text: '' });
const isSavingProfile = ref(false);
const isSavingPassword = ref(false);

onMounted(() => {
  if (authStore.user) {
    profileForm.first_name = authStore.user.first_name || '';
    profileForm.last_name = authStore.user.last_name || '';
    profileForm.username = authStore.user.username || '';
    profileForm.email = authStore.user.email || '';
  }
});

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];
    selectedFile.value = file;
    previewUrl.value = URL.createObjectURL(file);
  }
};

const handleUpdateProfile = async () => {
  if (!authStore.user?.id) return;
  isSavingProfile.value = true;
  profileMessage.value = { type: '', text: '' };

  try {
    const formData = new FormData();
    formData.append('first_name', profileForm.first_name);
    formData.append('last_name', profileForm.last_name);
    formData.append('username', profileForm.username);
    formData.append('email', profileForm.email);

    if (selectedFile.value) {
      formData.append('file', selectedFile.value);
    }

    const updatedUser = await userService.updateUser(authStore.user.id, formData);
    authStore.updateUserData((updatedUser as any).user || updatedUser);

    profileMessage.value = { type: 'success', text: 'Perfil actualizado correctamente.' };
  } catch (error: any) {
    profileMessage.value = {
      type: 'error',
      text: error.response?.data?.error || 'Error al actualizar el perfil.'
    };
  } finally {
    isSavingProfile.value = false;
  }
};

const handleChangePassword = async () => {
  passwordMessage.value = { type: '', text: '' };

  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordMessage.value = { type: 'error', text: 'Las nuevas contraseñas no coinciden.' };
    return;
  }

  if (passwordForm.new_password.length < 6) {
    passwordMessage.value = { type: 'error', text: 'La contraseña debe tener al menos 6 caracteres.' };
    return;
  }

  isSavingPassword.value = true;

  try {
    await userService.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    });

    passwordMessage.value = { type: 'success', text: 'Contraseña actualizada con éxito.' };
    passwordForm.current_password = '';
    passwordForm.new_password = '';
    passwordForm.confirm_password = '';
  } catch (error: any) {
    passwordMessage.value = {
      type: 'error',
      text: error.response?.data?.error || 'Error al cambiar la contraseña.'
    };
  } finally {
    isSavingPassword.value = false;
  }
};
</script>

<template>
  <div class="py-4 max-w-[860px] mx-auto space-y-6">
    <!-- Header Principal de la Página -->
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400 flex items-center justify-center shrink-0">
        <span class="material-symbols-outlined notranslate text-3xl">manage_accounts</span>
      </div>
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white leading-tight">Configuración de Perfil</h1>
        <p class="text-slate-500 dark:text-slate-400 text-xs">Administra tus datos personales y credenciales de acceso a la plataforma.</p>
      </div>
    </div>

    <!-- Sección 1: Información Personal -->
    <div class="bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border border-slate-200/80 dark:border-slate-800 shadow-sm rounded-3xl p-5 md:p-6 transition-all">
      <div class="flex items-center gap-2 mb-5 pb-3 border-b border-slate-100 dark:border-slate-800">
        <span class="material-symbols-outlined notranslate text-indigo-600 dark:text-indigo-400">person_gear</span>
        <h2 class="text-lg font-semibold notranslate text-slate-800 dark:text-slate-100">Información Personal</h2>
      </div>

      <!-- Banner de Alertas -->
      <div 
        v-if="profileMessage.text"
        :class="[
          'flex items-center gap-2.5 py-2.5 px-3.5 text-xs rounded-2xl mb-4 border transition-all',
          profileMessage.type === 'success'
            ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
            : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate text-lg shrink-0">
          {{ profileMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>
        <div class="font-medium">{{ profileMessage.text }}</div>
      </div>

      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <!-- Área de Carga de Avatar -->
        <div class="flex items-center gap-4 p-4 rounded-2xl bg-slate-50/80 dark:bg-slate-800/40 border border-dashed border-slate-200 dark:border-slate-700">
          <div class="relative shrink-0">
            <UserAvatar :src="previewUrl || authStore.avatarUrl" :alt="profileForm.username" size="lg" />
            <div class="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center border-2 border-white dark:border-slate-900 shadow-sm">
              <span class="material-symbols-outlined notranslate text-xs">photo_camera</span>
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <label for="avatarInput" class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1 flex items-center gap-1.5">
              <span class="material-symbols-outlined notranslate text-sm text-slate-400">image</span>
              Foto de perfil
            </label>
            <input 
              id="avatarInput" 
              type="file" 
              @change="handleFileChange" 
              accept="image/*" 
              class="block w-full text-xs text-slate-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-medium file:bg-indigo-50 file:text-indigo-600 hover:file:bg-indigo-100 dark:file:bg-indigo-950/50 dark:file:text-indigo-300 dark:hover:file:bg-indigo-900/50 file:transition-colors file:cursor-pointer cursor-pointer" 
            />
            <div class="text-[11px] text-slate-400 flex items-center gap-1 mt-1.5">
              <span class="material-symbols-outlined notranslate text-sm">info</span>
              Formatos recomendados: JPG, PNG. Tamaño máx: 2MB
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Nombre -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Nombre</label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">badge</span>
              </span>
              <input v-model="profileForm.first_name" type="text" class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="Tu nombre" />
            </div>
          </div>

          <!-- Apellido -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Apellido</label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">badge</span>
              </span>
              <input v-model="profileForm.last_name" type="text" class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="Tu apellido" />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Nombre de Usuario <span class="text-rose-500">*</span></label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">alternate_email</span>
              </span>
              <input v-model="profileForm.username" type="text" required class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="username" />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Correo Electrónico <span class="text-rose-500">*</span></label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">mail</span>
              </span>
              <input v-model="profileForm.email" type="email" required class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="correo@ejemplo.com" />
            </div>
          </div>
        </div>

        <!-- Botón de guardar perfil -->
        <div class="flex justify-end pt-2">
          <button 
            :disabled="isSavingProfile" 
            type="submit" 
            class="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-semibold bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-white transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed shadow-[0_4px_14px_rgba(15,23,42,0.25)] hover:-translate-y-0.5 active:translate-y-0"
          >
            <svg v-if="isSavingProfile" class="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="material-symbols-outlined notranslate text-lg" v-else>save</span>
            <span>{{ isSavingProfile ? 'Guardando...' : 'Guardar Cambios' }}</span>
          </button>
        </div>
      </form>
    </div>

    <!-- Sección 2: Seguridad y Contraseña -->
    <div class="bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border border-slate-200/80 dark:border-slate-800 shadow-sm rounded-3xl p-5 md:p-6 transition-all">
      <div class="flex items-center gap-2 mb-5 pb-3 border-b border-slate-100 dark:border-slate-800">
        <span class="material-symbols-outlined text-indigo-600 dark:text-indigo-400 notranslate">shield</span>
        <h2 class="text-lg font-semibold text-slate-800 dark:text-slate-100">Seguridad & Contraseña</h2>
      </div>

      <!-- Banner de Alertas de Contraseña -->
      <div 
        v-if="passwordMessage.text"
        :class="[
          'flex items-center gap-2.5 py-2.5 px-3.5 text-xs rounded-2xl mb-4 border transition-all',
          passwordMessage.type === 'success'
            ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20'
            : 'bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/20'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate text-lg shrink-0">
          {{ passwordMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>
        <div class="font-medium">{{ passwordMessage.text }}</div>
      </div>

      <form @submit.prevent="handleChangePassword" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Contraseña Actual -->
          <div class="md:col-span-2">
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Contraseña Actual <span class="text-rose-500">*</span></label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">lock</span>
              </span>
              <input v-model="passwordForm.current_password" type="password" required class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="••••••••" />
            </div>
          </div>

          <!-- Nueva Contraseña -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Nueva Contraseña <span class="text-rose-500">*</span></label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">password</span>
              </span>
              <input v-model="passwordForm.new_password" type="password" required class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="Mínimo 6 caracteres" />
            </div>
          </div>

          <!-- Confirmar Contraseña -->
          <div>
            <label class="block font-medium text-xs text-slate-700 dark:text-slate-300 mb-1">Confirmar Nueva Contraseña <span class="text-rose-500">*</span></label>
            <div class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:border-indigo-500 transition-all">
              <span class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
                <span class="material-symbols-outlined notranslate text-xl">enhanced_encryption</span>
              </span>
              <input v-model="passwordForm.confirm_password" type="password" required class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" placeholder="Repite la contraseña" />
            </div>
          </div>
        </div>

        <!-- Botón de actualizar contraseña -->
        <div class="flex justify-end pt-2">
          <button 
            :disabled="isSavingPassword" 
            type="submit" 
            class="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-semibold bg-indigo-600 text-white hover:bg-indigo-700 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed shadow-[0_4px_14px_rgba(79,70,229,0.35)] hover:-translate-y-0.5 active:translate-y-0"
          >
            <svg v-if="isSavingPassword" class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="material-symbols-outlined notranslate text-lg" v-else>vpn_key</span>
            <span>{{ isSavingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>