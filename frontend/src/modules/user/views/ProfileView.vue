<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { userService } from '../services/userService';
import UserAvatar from '@/layouts/components/UserAvatar.vue';
import AppCard from '@/shared/components/AppCard.vue';
import AppButton from '@/shared/components/AppButton.vue';
import AppInput from '@/shared/components/AppInput.vue';
import AppBadge from '@/shared/components/AppBadge.vue';

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
  <div class="tw-py-4 tw-max-w-[860px] tw-mx-auto tw-space-y-6">
    <!-- Header Principal de la Página -->
    <div class="tw-flex tw-items-center tw-gap-3">
      <div class="tw-w-12 tw-h-12 tw-rounded-2xl tw-bg-surface-container tw-text-primary tw-flex tw-items-center tw-justify-center tw-shrink-0">
        <span class="material-symbols-outlined notranslate tw-text-3xl">manage_accounts</span>
      </div>
      <div>
        <h1 class="tw-text-2xl tw-font-bold tw-text-on-surface tw-leading-tight">Configuración de Perfil</h1>
        <p class="tw-text-on-surface-variant tw-text-xs">Administra tus datos personales y credenciales de acceso a la plataforma.</p>
      </div>
    </div>

    <!-- Sección 1: Información Personal -->
    <AppCard variant="glass">
      <template #header>
        <div class="tw-flex tw-items-center tw-gap-2">
          <h2 class="tw-text-lg tw-font-semibold notranslate tw-text-on-surface">Información Personal</h2>
        </div>
      </template>

      <!-- Banner de Alertas -->
      <div
        v-if="profileMessage.text"
        :class="[
          'tw-flex tw-items-center tw-gap-2.5 tw-py-2.5 tw-px-3.5 tw-text-xs tw-rounded-2xl tw-mb-4 tw-border tw-transition-all',
          profileMessage.type === 'success'
            ? 'tw-bg-success-bg tw-text-success tw-border-success/20'
            : 'tw-bg-error-bg tw-text-error tw-border-error/20'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate tw-text-lg tw-shrink-0">
          {{ profileMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>
        <div class="tw-font-medium">{{ profileMessage.text }}</div>
      </div>

      <form @submit.prevent="handleUpdateProfile" class="tw-space-y-4">
        <!-- Área de Carga de Avatar -->
        <div class="tw-flex tw-items-center tw-gap-4 tw-p-4 tw-rounded-2xl tw-bg-surface-container-low/50 tw-border tw-border-dashed tw-border-outline-variant">
          <div class="tw-relative tw-shrink-0">
            <UserAvatar :src="previewUrl || authStore.avatarUrl" :alt="profileForm.username" size="lg" />
            <div class="tw-absolute -tw-bottom-1 -tw-right-1 tw-w-6 tw-h-6 tw-rounded-full tw-bg-primary tw-text-on-primary tw-flex tw-items-center tw-justify-center tw-border-2 tw-border-surface-container-lowest tw-shadow-sm">
              <span class="material-symbols-outlined notranslate tw-text-xs">photo_camera</span>
            </div>
          </div>
          <div class="tw-flex-1 tw-min-w-0">
            <label for="avatarInput" class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1 tw-flex tw-items-center tw-gap-1.5">
              <span class="material-symbols-outlined notranslate tw-text-sm tw-text-outline">image</span>
              Foto de perfil
            </label>
            <input
              id="avatarInput"
              type="file"
              @change="handleFileChange"
              accept="image/*"
              class="tw-block tw-w-full tw-text-xs tw-text-on-surface-variant file:tw-mr-3 file:tw-py-1.5 file:tw-px-3 file:tw-rounded-xl file:tw-border-0 file:tw-text-xs file:tw-font-medium file:tw-bg-surface-container file:tw-text-primary hover:file:tw-bg-surface-container-high file:tw-transition-colors file:tw-cursor-pointer tw-cursor-pointer"
            />
            <div class="tw-text-[11px] tw-text-outline tw-flex tw-items-center tw-gap-1 tw-mt-1.5">
              <span class="material-symbols-outlined notranslate tw-text-sm">info</span>
              Formatos recomendados: JPG, PNG. Tamaño máx: 2MB
            </div>
          </div>
        </div>

        <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Nombre</label>
            <AppInput v-model="profileForm.first_name" icon="badge" placeholder="Tu nombre" />
          </div>

          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Apellido</label>
            <AppInput v-model="profileForm.last_name" icon="badge" placeholder="Tu apellido" />
          </div>

          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Nombre de Usuario <span class="tw-text-error">*</span></label>
            <AppInput v-model="profileForm.username" icon="alternate_email" placeholder="username" />
          </div>

          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Correo Electrónico <span class="tw-text-error">*</span></label>
            <AppInput v-model="profileForm.email" type="email" icon="mail" placeholder="correo@ejemplo.com" />
          </div>
        </div>

        <!-- Botón de guardar perfil -->
        <div class="tw-flex tw-justify-end tw-pt-2">
          <AppButton type="submit" variant="primary" :loading="isSavingProfile" icon="save">
            {{ isSavingProfile ? 'Guardando...' : 'Guardar Cambios' }}
          </AppButton>
        </div>
      </form>
    </AppCard>

    <!-- Sección 2: Seguridad y Contraseña -->
    <AppCard variant="glass">
      <template #header>
        <div class="tw-flex tw-items-center tw-gap-2">
          <span class="material-symbols-outlined tw-text-primary notranslate">shield</span>
          <h2 class="tw-text-lg tw-font-semibold tw-text-on-surface">Seguridad &amp; Contraseña</h2>
        </div>
      </template>

      <!-- Banner de Alertas de Contraseña -->
      <div
        v-if="passwordMessage.text"
        :class="[
          'tw-flex tw-items-center tw-gap-2.5 tw-py-2.5 tw-px-3.5 tw-text-xs tw-rounded-2xl tw-mb-4 tw-border tw-transition-all',
          passwordMessage.type === 'success'
            ? 'tw-bg-success-bg tw-text-success tw-border-success/20'
            : 'tw-bg-error-bg tw-text-error tw-border-error/20'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate tw-text-lg tw-shrink-0">
          {{ passwordMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>
        <div class="tw-font-medium">{{ passwordMessage.text }}</div>
      </div>

      <form @submit.prevent="handleChangePassword" class="tw-space-y-4">
        <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
          <!-- Contraseña Actual -->
          <div class="md:tw-col-span-2">
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Contraseña Actual <span class="tw-text-error">*</span></label>
            <AppInput v-model="passwordForm.current_password" type="password" icon="lock" placeholder="••••••••" />
          </div>

          <!-- Nueva Contraseña -->
          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Nueva Contraseña <span class="tw-text-error">*</span></label>
            <AppInput v-model="passwordForm.new_password" type="password" icon="password" placeholder="Mínimo 6 caracteres" />
          </div>

          <!-- Confirmar Contraseña -->
          <div>
            <label class="tw-block tw-font-medium tw-text-xs tw-text-on-surface-variant tw-mb-1">Confirmar Nueva Contraseña <span class="tw-text-error">*</span></label>
            <AppInput v-model="passwordForm.confirm_password" type="password" icon="enhanced_encryption" placeholder="Repite la contraseña" />
          </div>
        </div>

        <!-- Botón de actualizar contraseña -->
        <div class="tw-flex tw-justify-end tw-pt-2">
          <AppButton type="submit" variant="primary" :loading="isSavingPassword" icon="vpn_key">
            {{ isSavingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}
          </AppButton>
        </div>
      </form>
    </AppCard>
  </div>
</template>