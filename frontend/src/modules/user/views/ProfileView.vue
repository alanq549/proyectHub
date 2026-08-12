<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { userService } from '../services/userService'
import UserAvatar from '@/layouts/components/UserAvatar.vue'
import AppCard from '@/shared/components/AppCard.vue'
import AppButton from '@/shared/components/AppButton.vue'
import AppInput from '@/shared/components/AppInput.vue'

const authStore = useAuthStore()

const profileForm = reactive({
  first_name: '',
  last_name: '',
  username: '',
  email: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

const profileMessage = ref({
  type: '',
  text: ''
})

const passwordMessage = ref({
  type: '',
  text: ''
})

const isSavingProfile = ref(false)
const isSavingPassword = ref(false)

onMounted(() => {
  if (!authStore.user) return

  profileForm.first_name = authStore.user.first_name || ''
  profileForm.last_name = authStore.user.last_name || ''
  profileForm.username = authStore.user.username || ''
  profileForm.email = authStore.user.email || ''
})

onBeforeUnmount(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  // Validación básica
  if (!file.type.startsWith('image/')) {
    profileMessage.value = {
      type: 'error',
      text: 'El archivo seleccionado debe ser una imagen.'
    }
    target.value = ''
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    profileMessage.value = {
      type: 'error',
      text: 'La imagen no puede superar los 2 MB.'
    }
    target.value = ''
    return
  }

  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }

  selectedFile.value = file
  previewUrl.value = URL.createObjectURL(file)

  profileMessage.value = {
    type: '',
    text: ''
  }
}

const handleUpdateProfile = async () => {
  if (!authStore.user?.id) return

  profileMessage.value = {
    type: '',
    text: ''
  }

  if (!profileForm.username.trim() || !profileForm.email.trim()) {
    profileMessage.value = {
      type: 'error',
      text: 'El nombre de usuario y el correo electrónico son obligatorios.'
    }
    return
  }

  isSavingProfile.value = true

  try {
    const formData = new FormData()

    formData.append('first_name', profileForm.first_name.trim())
    formData.append('last_name', profileForm.last_name.trim())
    formData.append('username', profileForm.username.trim())
    formData.append('email', profileForm.email.trim())

    if (selectedFile.value) {
      formData.append('file', selectedFile.value)
    }

    const updatedUser = await userService.updateUser(
      authStore.user.id,
      formData
    )

    const userData = (updatedUser as any).user || updatedUser

    authStore.updateUserData(userData)

    profileMessage.value = {
      type: 'success',
      text: 'Tu información de perfil se actualizó correctamente.'
    }

    selectedFile.value = null
  } catch (error: any) {
    profileMessage.value = {
      type: 'error',
      text:
        error.response?.data?.error ||
        error.response?.data?.message ||
        'No fue posible actualizar tu perfil.'
    }
  } finally {
    isSavingProfile.value = false
  }
}

const handleChangePassword = async () => {
  passwordMessage.value = {
    type: '',
    text: ''
  }

  if (!passwordForm.current_password) {
    passwordMessage.value = {
      type: 'error',
      text: 'Ingresa tu contraseña actual.'
    }
    return
  }

  if (passwordForm.new_password.length < 6) {
    passwordMessage.value = {
      type: 'error',
      text: 'La nueva contraseña debe tener al menos 6 caracteres.'
    }
    return
  }

  if (passwordForm.new_password !== passwordForm.confirm_password) {
    passwordMessage.value = {
      type: 'error',
      text: 'Las nuevas contraseñas no coinciden.'
    }
    return
  }

  isSavingPassword.value = true

  try {
    await userService.changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password
    })

    passwordMessage.value = {
      type: 'success',
      text: 'Tu contraseña se actualizó correctamente.'
    }

    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (error: any) {
    passwordMessage.value = {
      type: 'error',
      text:
        error.response?.data?.error ||
        error.response?.data?.message ||
        'No fue posible cambiar la contraseña.'
    }
  } finally {
    isSavingPassword.value = false
  }
}
</script>

<template>
  <div class="tw-relative tw-max-w-[900px] tw-mx-auto tw-py-6 sm:tw-py-8 tw-space-y-6">

    <!-- Decoración de fondo -->
    <div
      class="tw-pointer-events-none tw-absolute tw--top-20 tw-left-1/2 tw--translate-x-1/2 tw-w-[520px] tw-h-[520px] tw-rounded-full tw-blur-3xl tw-opacity-[0.06]"
      style="background: radial-gradient(circle, var(--color-primary) 0%, transparent 70%);"
    />

    <!-- ========================================================= -->
    <!-- HEADER -->
    <!-- ========================================================= -->

    <header class="tw-relative tw-flex tw-items-start tw-justify-between tw-gap-4">
      <div class="tw-space-y-3">

        <div class="tw-flex tw-items-center tw-gap-2">
          <span class="tw-h-px tw-w-7 tw-bg-primary/60"></span>

          <span
            class="tw-text-[10px] tw-font-bold tw-uppercase tw-tracking-[0.2em] tw-text-primary"
          >
            Mi cuenta
          </span>
        </div>

        <div class="tw-flex tw-items-center tw-gap-3">
          <div
            class="tw-flex tw-h-11 tw-w-11 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-xl tw-bg-primary tw-text-on-primary tw-shadow-lg"
          >
            <span class="material-symbols-outlined notranslate tw-text-2xl">
              manage_accounts
            </span>
          </div>

          <div>
            <h1
              class="tw-text-2xl tw-font-bold tw-leading-tight tw-text-on-surface"
            >
              Configuración de Perfil
            </h1>

            <p
              class="tw-mt-1 tw-text-xs tw-text-on-surface-variant"
            >
              Administra tu información personal y la seguridad de tu cuenta.
            </p>
          </div>
        </div>
      </div>
    </header>


    <!-- ========================================================= -->
    <!-- INFORMACIÓN PERSONAL -->
    <!-- ========================================================= -->

    <AppCard
      variant="glass"
      class="tw-relative tw-overflow-hidden tw-border tw-border-outline-variant/60 tw-bg-surface-container/80 tw-backdrop-blur-xl"
    >
      <!-- Línea superior decorativa -->
      <div
        class="tw-absolute tw-left-0 tw-right-0 tw-top-0 tw-h-px tw-bg-gradient-to-r tw-from-transparent tw-via-primary/50 tw-to-transparent"
      />

      <template #header>
        <div class="tw-flex tw-items-center tw-justify-between tw-gap-3">
          <div class="tw-flex tw-items-center tw-gap-3">
            <div
              class="tw-flex tw-h-9 tw-w-9 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10 tw-text-primary"
            >
              <span class="material-symbols-outlined notranslate tw-text-xl">
                person
              </span>
            </div>

            <div>
              <h2 class="tw-text-base tw-font-bold tw-text-on-surface">
                Información Personal
              </h2>

              <p class="tw-text-[11px] tw-text-on-surface-variant">
                Actualiza los datos asociados a tu cuenta.
              </p>
            </div>
          </div>
        </div>
      </template>


      <!-- Mensaje -->
      <div
        v-if="profileMessage.text"
        :class="[
          'tw-mb-5 tw-flex tw-items-start tw-gap-3 tw-rounded-xl tw-border tw-p-3',
          profileMessage.type === 'success'
            ? 'tw-border-success/20 tw-bg-success-bg/60 tw-text-success'
            : 'tw-border-error/20 tw-bg-error-bg/60 tw-text-error'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate tw-text-lg">
          {{ profileMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>

        <div class="tw-flex-1 tw-text-xs tw-font-medium">
          {{ profileMessage.text }}
        </div>
      </div>


      <form
        @submit.prevent="handleUpdateProfile"
        class="tw-space-y-5"
      >

        <!-- ===================================================== -->
        <!-- AVATAR -->
        <!-- ===================================================== -->

        <div
          class="tw-flex tw-flex-col sm:tw-flex-row tw-items-center sm:tw-items-start tw-gap-5 tw-rounded-2xl tw-border tw-border-outline-variant/50 tw-bg-surface-container-low/60 tw-p-5"
        >
          <div class="tw-relative tw-shrink-0">
            <UserAvatar
              :src="previewUrl || authStore.avatarUrl"
              :alt="profileForm.username || 'Usuario'"
              size="lg"
            />

            <div
              class="tw-absolute -tw-bottom-1 -tw-right-1 tw-flex tw-h-7 tw-w-7 tw-items-center tw-justify-center tw-rounded-full tw-border-2 tw-border-surface-container tw-bg-primary tw-text-on-primary tw-shadow-md"
            >
              <span class="material-symbols-outlined notranslate tw-text-sm">
                photo_camera
              </span>
            </div>
          </div>

          <div class="tw-min-w-0 tw-flex-1 tw-text-center sm:tw-text-left">
            <h3 class="tw-text-sm tw-font-bold tw-text-on-surface">
              Foto de perfil
            </h3>

            <p class="tw-mt-1 tw-text-xs tw-text-on-surface-variant">
              Utiliza una imagen clara para identificar tu cuenta.
            </p>

            <label
              for="avatarInput"
              class="tw-mt-3 tw-inline-flex tw-cursor-pointer tw-items-center tw-gap-2 tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container tw-px-3 tw-py-2 tw-text-xs tw-font-semibold tw-text-on-surface hover:tw-border-primary/40 hover:tw-bg-primary/5 tw-transition-all"
            >
              <span class="material-symbols-outlined notranslate tw-text-base">
                upload
              </span>

              Seleccionar imagen
            </label>

            <input
              id="avatarInput"
              type="file"
              accept="image/png,image/jpeg,image/webp"
              @change="handleFileChange"
              class="tw-hidden"
            />

            <div
              class="tw-mt-2 tw-flex tw-items-center tw-justify-center sm:tw-justify-start tw-gap-1.5 tw-text-[10px] tw-text-outline"
            >
              <span class="material-symbols-outlined notranslate tw-text-sm">
                info
              </span>

              JPG, PNG o WEBP · Máximo 2 MB
            </div>
          </div>
        </div>


        <!-- ===================================================== -->
        <!-- CAMPOS -->
        <!-- ===================================================== -->

        <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">

          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Nombre
            </label>

            <AppInput
              v-model="profileForm.first_name"
              icon="badge"
              placeholder="Tu nombre"
            />
          </div>


          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Apellido
            </label>

            <AppInput
              v-model="profileForm.last_name"
              icon="badge"
              placeholder="Tu apellido"
            />
          </div>


          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Nombre de usuario
              <span class="tw-text-primary">*</span>
            </label>

            <AppInput
              v-model="profileForm.username"
              icon="alternate_email"
              placeholder="username"
            />
          </div>


          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Correo electrónico
              <span class="tw-text-primary">*</span>
            </label>

            <AppInput
              v-model="profileForm.email"
              type="email"
              icon="mail"
              placeholder="correo@ejemplo.com"
            />
          </div>

        </div>


        <!-- Guardar -->
        <div
          class="tw-flex tw-flex-col sm:tw-flex-row tw-items-center tw-justify-between tw-gap-3 tw-border-t tw-border-outline-variant/40 tw-pt-4"
        >
          <div
            class="tw-flex tw-items-center tw-gap-2 tw-text-[11px] tw-text-on-surface-variant"
          >
            <span class="material-symbols-outlined notranslate tw-text-sm">
              verified_user
            </span>

            Tus datos se almacenan de forma segura.
          </div>

          <AppButton
            type="submit"
            variant="primary"
            :loading="isSavingProfile"
            icon="save"
          >
            {{ isSavingProfile ? 'Guardando...' : 'Guardar Cambios' }}
          </AppButton>
        </div>

      </form>
    </AppCard>


    <!-- ========================================================= -->
    <!-- SEGURIDAD -->
    <!-- ========================================================= -->

    <AppCard
      variant="glass"
      class="tw-relative tw-overflow-hidden tw-border tw-border-outline-variant/60 tw-bg-surface-container/80 tw-backdrop-blur-xl"
    >

      <div
        class="tw-absolute tw-left-0 tw-right-0 tw-top-0 tw-h-px tw-bg-gradient-to-r tw-from-transparent tw-via-primary/40 tw-to-transparent"
      />

      <template #header>
        <div class="tw-flex tw-items-center tw-gap-3">

          <div
            class="tw-flex tw-h-9 tw-w-9 tw-items-center tw-justify-center tw-rounded-lg tw-bg-primary/10 tw-text-primary"
          >
            <span class="material-symbols-outlined notranslate tw-text-xl">
              shield
            </span>
          </div>

          <div>
            <h2 class="tw-text-base tw-font-bold tw-text-on-surface">
              Seguridad de la cuenta
            </h2>

            <p class="tw-text-[11px] tw-text-on-surface-variant">
              Mantén protegidas tus credenciales de acceso.
            </p>
          </div>

        </div>
      </template>


      <!-- Mensaje -->
      <div
        v-if="passwordMessage.text"
        :class="[
          'tw-mb-5 tw-flex tw-items-start tw-gap-3 tw-rounded-xl tw-border tw-p-3',
          passwordMessage.type === 'success'
            ? 'tw-border-success/20 tw-bg-success-bg/60 tw-text-success'
            : 'tw-border-error/20 tw-bg-error-bg/60 tw-text-error'
        ]"
        role="alert"
      >
        <span class="material-symbols-outlined notranslate tw-text-lg">
          {{ passwordMessage.type === 'success' ? 'check_circle' : 'error' }}
        </span>

        <div class="tw-flex-1 tw-text-xs tw-font-medium">
          {{ passwordMessage.text }}
        </div>
      </div>


      <!-- Info de seguridad -->
      <div
        class="tw-mb-5 tw-flex tw-items-start tw-gap-3 tw-rounded-xl tw-border tw-border-primary/15 tw-bg-primary/5 tw-p-4"
      >
        <span
          class="material-symbols-outlined notranslate tw-text-primary tw-text-xl"
        >
          lock
        </span>

        <div>
          <p class="tw-text-xs tw-font-bold tw-text-on-surface">
            Cambia tu contraseña periódicamente
          </p>

          <p class="tw-mt-1 tw-text-[11px] tw-leading-relaxed tw-text-on-surface-variant">
            Utiliza una contraseña única y evita compartir tus credenciales con otras personas.
          </p>
        </div>
      </div>


      <form
        @submit.prevent="handleChangePassword"
        class="tw-space-y-5"
      >

        <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">

          <!-- Contraseña actual -->
          <div class="md:tw-col-span-2">
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Contraseña actual
              <span class="tw-text-primary">*</span>
            </label>

            <AppInput
              v-model="passwordForm.current_password"
              type="password"
              icon="lock"
              placeholder="Ingresa tu contraseña actual"
            />
          </div>


          <!-- Nueva -->
          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Nueva contraseña
              <span class="tw-text-primary">*</span>
            </label>

            <AppInput
              v-model="passwordForm.new_password"
              type="password"
              icon="password"
              placeholder="Mínimo 6 caracteres"
            />

            <p
              class="tw-mt-1.5 tw-text-[10px] tw-text-on-surface-variant"
            >
              Usa al menos 6 caracteres.
            </p>
          </div>


          <!-- Confirmación -->
          <div>
            <label
              class="tw-mb-1.5 tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant"
            >
              Confirmar contraseña
              <span class="tw-text-primary">*</span>
            </label>

            <AppInput
              v-model="passwordForm.confirm_password"
              type="password"
              icon="enhanced_encryption"
              placeholder="Repite la contraseña"
            />

            <p
              v-if="
                passwordForm.confirm_password &&
                passwordForm.new_password !== passwordForm.confirm_password
              "
              class="tw-mt-1.5 tw-flex tw-items-center tw-gap-1 tw-text-[10px] tw-text-error"
            >
              <span class="material-symbols-outlined notranslate tw-text-xs">
                error
              </span>

              Las contraseñas no coinciden.
            </p>

            <p
              v-else-if="
                passwordForm.confirm_password &&
                passwordForm.new_password === passwordForm.confirm_password
              "
              class="tw-mt-1.5 tw-flex tw-items-center tw-gap-1 tw-text-[10px] tw-text-success"
            >
              <span class="material-symbols-outlined notranslate tw-text-xs">
                check_circle
              </span>

              Las contraseñas coinciden.
            </p>
          </div>

        </div>


        <!-- Actualizar contraseña -->
        <div
          class="tw-flex tw-flex-col sm:tw-flex-row tw-items-center tw-justify-between tw-gap-3 tw-border-t tw-border-outline-variant/40 tw-pt-4"
        >
          <div
            class="tw-flex tw-items-center tw-gap-2 tw-text-[11px] tw-text-on-surface-variant"
          >
            <span class="material-symbols-outlined notranslate tw-text-sm">
              security
            </span>

            Protege tu cuenta con una contraseña segura.
          </div>

          <AppButton
            type="submit"
            variant="primary"
            :loading="isSavingPassword"
            icon="vpn_key"
          >
            {{ isSavingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}
          </AppButton>
        </div>

      </form>
    </AppCard>


    <!-- Footer -->
    <div
      class="tw-flex tw-items-center tw-justify-center tw-gap-2 tw-py-2 tw-text-[10px] tw-text-outline"
    >
      <span class="material-symbols-outlined notranslate tw-text-sm">
        verified
      </span>

      Información protegida por los mecanismos de seguridad de ProjectHub.
    </div>

  </div>
</template>