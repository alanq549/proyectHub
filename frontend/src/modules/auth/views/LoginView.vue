<template>
  <div class="login-wrapper tw-min-h-screen tw-flex tw-items-center tw-justify-center tw-p-3 md:tw-p-0 tw-relative tw-overflow-hidden">

    <div class="bg-layer">
      <div class="blob-1"></div>
      <div class="blob-2"></div>
    </div>

    <main class="auth-card">
      <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2">
        <AuthSidebar />

        <!-- RIGHT PANEL -->
        <div class="tw-col-span-1 md:tw-col-span-1 right-panel">
          <div class="tw-mx-auto" style="max-width:24rem;">
            <AuthLoginMobileHeader />

            <!-- DESKTOP BACK BUTTON -->
            <div class="tw-hidden md:tw-block tw-mb-4">
              <button class="btn-back-home" @click="router.push({ name: 'home' })">
                Volver al inicio
              </button>
            </div>

            <div class="tw-mb-4">
              <h2 class="form-title tw-mb-2">
                Bienvenido de nuevo
              </h2>

              <p class="form-subtitle tw-mb-0">
                Ingresa tus credenciales para acceder.
              </p>
            </div>

            <!-- Alerta de Error Global / Backend -->
            <ErrorAlert v-if="errorMessage" :errorMessage="errorMessage" class="tw-mb-3" />

            <form id="login-form" @submit.prevent="handleLogin" class="tw-flex tw-flex-col tw-gap-3" novalidate>
              <!-- Input Email -->
              <div class="form-group">
                <label class="form-label-custom tw-mb-1 tw-block">Correo Electrónico</label>
                <div class="input-icon-wrap">
                  <span class="material-symbols-outlined notranslate">mail</span>
                  <input 
                    v-model.trim="email" 
                    type="email" 
                    class="form-control-custom tw-w-full"
                    :class="{ 'is-invalid': errors.email }"
                    placeholder="correo@universidad.edu" 
                    @input="clearFieldError('email')"
                  />
                </div>
                <div v-if="errors.email" class="invalid-feedback tw-block tw-mt-1">
                  {{ errors.email }}
                </div>
              </div>

              <!-- Input Password -->
              <div class="tw-flex tw-flex-col tw-gap-1">
                <div class="tw-flex tw-justify-between tw-items-center tw-mb-1">
                  <label class="form-label-custom tw-mb-0">Contraseña</label>
                </div>
                <div class="input-icon-wrap">
                  <span class="material-symbols-outlined notranslate">lock</span>
                  <input 
                    v-model="password" 
                    :type="showPassword ? 'text' : 'password'" 
                    class="form-control-custom has-toggle tw-w-full"
                    :class="{ 'is-invalid': errors.password }"
                    placeholder="••••••••"
                    @input="clearFieldError('password')"
                  />
                  <button type="button" class="toggle-icon" @click="togglePassword">
                    <span class="material-symbols-outlined notranslate tw-text-xl">
                      {{ showPassword ? 'visibility_off' : 'visibility' }}
                    </span>
                  </button>
                </div>
                <div v-if="errors.password" class="invalid-feedback tw-block tw-mt-1">
                  {{ errors.password }}
                </div>
              </div>

              <!-- Botón Iniciar Sesión -->
              <button type="submit" class="btn-primary-custom tw-mt-2" :disabled="isLoading">
                <span v-if="!isLoading">Iniciar Sesión</span>
                <span v-else class="tw-inline-block tw-h-4 tw-w-4 tw-animate-spin tw-rounded-full tw-border-2 tw-border-current tw-border-t-transparent" role="status"></span>
              </button>
            </form>

            <div class="tw-text-center tw-mt-4">
              <p class="form-subtitle tw-mb-0">
                ¿No tienes una cuenta?
                <a href="#" class="tw-text-primary tw-font-semibold tw-no-underline hover:tw-underline tw-transition-all" @click.prevent="router.push({ name: 'register' })">
                  Crear cuenta
                </a>
              </p>
            </div>
            
            <SSOButtons />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

import AuthSidebar from '@/modules/auth/components/AuthSidebar.vue'
import AuthLoginMobileHeader from '@/modules/auth/components/AuthLoginMobileHeader.vue'
import ErrorAlert from '@/modules/auth/components/ErrorAlert.vue'
import SSOButtons from '@/modules/auth/components/SSOButtons.vue'

const router = useRouter()
const authStore = useAuthStore()

// Campos del formulario
const email = ref('')
const password = ref('')

// Objeto reactivo de errores por campo
const errors = reactive({
  email: '',
  password: ''
})

// Estados de la UI
const showPassword = ref(false)
const isLoading = ref(false)
const errorMessage = ref('')

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const clearFieldError = (field: 'email' | 'password') => {
  errors[field] = ''
}

// Regex para validación de email
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Validación programática antes de enviar
const validateForm = (): boolean => {
  let isValid = true;
  errors.email = ''
  errors.password = ''

  if (!email.value) {
    errors.email = 'El correo electrónico es obligatorio.'
    isValid = false
  } else if (!emailRegex.test(email.value)) {
    errors.email = 'Ingresa un formato de correo electrónico válido.'
    isValid = false
  }

  if (!password.value) {
    errors.password = 'La contraseña es obligatoria.'
    isValid = false
  }

  return isValid
}

// Disparar animación de sacudida en caso de error
const triggerShakeAnimation = () => {
  const form = document.getElementById('login-form')
  if (form) {
    form.classList.add('animate-shake')
    setTimeout(() => {
      form.classList.remove('animate-shake')
    }, 500)
  }
}

// Petición Real al Backend Flask mediante el AuthStore
const handleLogin = async () => {
  errorMessage.value = ''
  
  if (!validateForm()) {
    triggerShakeAnimation()
    return
  }

  isLoading.value = true

  try {
    await authStore.login({
      email: email.value,
      password: password.value
    })

    if (authStore.isAdmin) {
      router.push({ name: 'users-list' })
    } else {
      router.push({ name: 'dashboard' })
    }
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || error.response?.data?.error || 'Correo o contraseña incorrectos. Inténtalo de nuevo.'
    triggerShakeAnimation()
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Variables moved to global CSS or handled by a theme */
/* .login-wrapper background color */
.login-wrapper {
  background-color: var(--background, #f7f9fb);
}

/* Background atmospheric layer */
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  background-color: var(--surface-bright, #f7f9fb);
}

.bg-layer::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(75, 65, 225, 0.05) 0%, transparent 40%),
    radial-gradient(circle at bottom left, rgba(172, 237, 255, 0.05) 0%, transparent 40%);
}

.blob-1 {
  position: absolute;
  top: -10%;
  right: -5%;
  width: 40%;
  height: 40%;
  background: rgba(75, 65, 225, 0.05);
  border-radius: 50%;
  filter: blur(120px);
}

.blob-2 {
  position: absolute;
  bottom: -10%;
  left: -5%;
  width: 30%;
  height: 30%;
  background: rgba(76, 215, 246, 0.10);
  border-radius: 50%;
  filter: blur(100px);
}

.auth-card {
  position: relative;
  z-index: 10;
  max-width: 1100px;
  width: 100%;
  border-radius: 2rem;
  overflow: hidden;
  box-shadow: 0px 40px 100px rgba(0, 0, 0, 0.06);
  background: #fff;
}

/* Left panel */


/* Right panel (form) */
.right-panel {
  background-color: var(--surface-container-lowest, #ffffff);
  padding: 64px;
}


@media (max-width: 767.98px) {
  .right-panel {
    padding: 2rem;
  }
}

.form-title {
  color: var(--on-surface, #191c1e);
  font-weight: 600;
  letter-spacing: -0.01em;
  font-size: 24px;
}

@media (min-width: 768px) {
  .form-title {
    font-size: 32px;
    letter-spacing: -0.015em;
  }
}

.form-subtitle {
  color: var(--on-surface-variant, #45464d);
  font-size: 16px;
}

.form-label-custom {
  color: var(--on-surface-variant, #45464d);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.input-icon-wrap {
  position: relative;
}

/* Icono izquierdo (candado) */
.input-icon-wrap > .material-symbols-outlined {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--outline, #76777d);
  pointer-events: none;
}


/* Botón de mostrar/ocultar contraseña */
.toggle-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 32px;
  height: 32px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--outline-variant, #c6c6cd);
  cursor: pointer;
  background: transparent;
  border: none;
}


/* Icono dentro del botón */
.toggle-icon .material-symbols-outlined {
  font-size: 20px;
  line-height: 1;
}


.form-control-custom {
  height: 48px;
  padding-left: 48px;
  padding-right: 16px;
  background-color: var(--surface, #f7f9fb);
  border: 1px solid var(--outline-variant, #c6c6cd);
  border-radius: 0.75rem;
  color: var(--on-surface, #191c1e);
  font-size: 16px;
}

.form-control-custom.has-toggle {
  padding-right: 48px;
}

.form-control-custom:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(75, 65, 225, 0.10);
  border-color: var(--secondary, #4b41e1);
}

.form-control-custom.is-invalid {
  border-color: var(--app-error);
}

.invalid-feedback {
  color: var(--app-error);
  font-size: 0.75rem;
}

.btn-primary-custom {
  height: 52px;
  width: 100%;
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
  border-radius: 0.75rem;
  font-size: 14px;
  font-weight: 600;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: opacity .15s ease, transform .1s ease;
}

.btn-primary-custom:hover {
  opacity: 0.9;
  color: var(--on-primary, #ffffff);
}

.btn-primary-custom:active {
  transform: scale(0.98);
}

.btn-primary-custom:disabled {
  opacity: 0.9;
}


@keyframes shake {

  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-4px);
  }

  75% {
    transform: translateX(4px);
  }
}

.animate-shake {
  animation: shake 0.2s cubic-bezier(.36, .07, .19, .97) both;
}
</style>
