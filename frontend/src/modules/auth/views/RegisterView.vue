<template>
  <div class="registration-wrapper">
    <div class="bg-blobs">
      <div class="blob-a"></div>
      <div class="blob-b"></div>
    </div>

    <main class="main-wrap">
      <div class="tw-grid tw-grid-cols-1 lg:tw-grid-cols-12 tw-h-full">
        <AuthRegisterSidebar />

        <!-- Registration Section -->
        <div class="tw-col-span-1 lg:tw-col-span-7 form-section">
          <div class="tw-w-full form-container" style="max-width: 480px;">
            <AuthRegisterMobileHeader />

            <!-- Register Form -->
            <div v-if="!registrationSuccess">
              <header class="tw-mb-4">
                <h2 class="reg-title tw-mb-2">Crear una cuenta</h2>
                <p class="reg-subtitle tw-mb-0">
                  Ingresa tus datos para comenzar tu trayecto académico.
                </p>
              </header>

              <!-- Mensaje de error global -->
              <div v-if="errorMessage" class="tw-py-2 tw-text-xs tw-mb-3" role="alert" style="padding: 1rem; border-radius: 0.5rem; background-color: rgba(255, 218, 214, 0.5); border: 1px solid rgba(186, 26, 26, 0.10); color: var(--on-error-container, #93000a);">
                {{ errorMessage }}
              </div>

              <form @submit.prevent="handleRegistration" novalidate>
                <!-- Nombres y Apellidos -->
                <div class="tw-grid tw-grid-cols-2 tw-gap-2 tw-mb-3">
                  <div class="tw-col-span-1">
                    <label class="form-label-custom">Nombre(s)</label>
                    <div class="input-icon-wrap">
                      <span class="material-symbols-outlined notranslate icon-left">badge</span>
                      <input
                        v-model.trim="firstName"
                        type="text"
                        class="form-control-custom"
                        :class="{ 'is-invalid': fieldErrors.firstName, 'is-valid': firstName && !fieldErrors.firstName }"
                        placeholder="ej. Alan"
                        @blur="validateFirstName"
                        @input="fieldErrors.firstName = ''"
                        required
                      />
                    </div>
                    <div v-if="fieldErrors.firstName" class="invalid-feedback tw-block tw-mt-1">
                      {{ fieldErrors.firstName }}
                    </div>
                  </div>

                  <div class="tw-col-span-1">
                    <label class="form-label-custom">Apellido(s)</label>
                    <div class="input-icon-wrap">
                      <span class="material-symbols-outlined notranslate icon-left">badge</span>
                      <input
                        v-model.trim="lastName"
                        type="text"
                        class="form-control-custom"
                        :class="{ 'is-invalid': fieldErrors.lastName, 'is-valid': lastName && !fieldErrors.lastName }"
                        placeholder="ej. Arriaga"
                        @blur="validateLastName"
                        @input="fieldErrors.lastName = ''"
                        required
                      />
                    </div>
                    <div v-if="fieldErrors.lastName" class="invalid-feedback tw-block tw-mt-1">
                      {{ fieldErrors.lastName }}
                    </div>
                  </div>
                </div>

                <!-- Username -->
                <div class="tw-mb-3">
                  <label class="form-label-custom">Nombre de usuario</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined notranslate icon-left">person</span>
                    <input
                      v-model.trim="username"
                      type="text"
                      class="form-control-custom"
                      :class="{ 'is-invalid': fieldErrors.username, 'is-valid': username && !fieldErrors.username }"
                      placeholder="ej. alan_dev"
                      @blur="validateUsername"
                      @input="fieldErrors.username = ''"
                      required
                    />
                  </div>
                  <div v-if="fieldErrors.username" class="invalid-feedback tw-block tw-mt-1">
                    {{ fieldErrors.username }}
                  </div>
                </div>

                <!-- Email -->
                <div class="tw-mb-3">
                  <label class="form-label-custom">Correo electrónico</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined notranslate icon-left">mail</span>
                    <input
                      v-model.trim="email"
                      type="email"
                      class="form-control-custom"
                      :class="{ 'is-invalid': fieldErrors.email, 'is-valid': email && !fieldErrors.email }"
                      placeholder="correo@universidad.edu"
                      @blur="validateEmail"
                      @input="fieldErrors.email = ''"
                      required
                    />
                  </div>
                  <div v-if="fieldErrors.email" class="invalid-feedback tw-block tw-mt-1">
                    {{ fieldErrors.email }}
                  </div>
                </div>

                <!-- Password -->
                <div class="tw-mb-3">
                  <label class="form-label-custom">Contraseña</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined notranslate icon-left">lock</span>
                    <input
                      v-model="password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control-custom has-toggle"
                      :class="{ 'is-invalid': fieldErrors.password, 'is-valid': password && !fieldErrors.password }"
                      placeholder="••••••••"
                      @input="onPasswordInput"
                      @blur="validatePassword"
                      required
                    />
                    <button type="button" class="toggle-icon" @click="togglePassword">
                      <span class="material-symbols-outlined notranslate">
                        {{ showPassword ? 'visibility_off' : 'visibility' }}
                      </span>
                    </button>
                  </div>
                  <div v-if="fieldErrors.password" class="invalid-feedback tw-block tw-mt-1">
                    {{ fieldErrors.password }}
                  </div>

                  <!-- Indicador de Fuerza de Contraseña -->
                  <div class="tw-pt-2">
                    <div class="strength-row tw-flex tw-justify-between tw-items-center tw-mb-1">
                      <span class="strength-text text-xs text-slate-500">Seguridad de la contraseña</span>
                      <span class="strength-label tw-text-xs tw-font-bold" :style="{ color: strengthColor }">
                        {{ strengthText }}
                      </span>
                    </div>
                    <div class="strength-track tw-rounded tw-overflow-hidden" style="height: 6px; background-color: var(--outline-variant, #e0e0e0);">
                      <div
                        class="password-strength-bar"
                        :style="{
                          width: strength + '%',
                          backgroundColor: strengthColor,
                          height: '100%',
                          transition: 'width 0.3s ease, background-color 0.3s ease'
                        }"
                      ></div>
                    </div>
                  </div>
                </div>

                <!-- Confirm Password -->
                <div class="tw-mb-3">
                  <label class="form-label-custom">Confirmar contraseña</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined notranslate icon-left">verified_user</span>
                    <input
                      v-model="confirmPassword"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control-custom has-toggle"
                      :class="{ 'is-invalid': fieldErrors.confirmPassword, 'is-valid': confirmPassword && !fieldErrors.confirmPassword }"
                      placeholder="••••••••"
                      @input="onConfirmPasswordInput"
                      @blur="validateConfirmPassword"
                      required
                    />
                    <button type="button" class="toggle-icon" @click="toggleConfirmPassword">
                      <span class="material-symbols-outlined notranslate">
                        {{ showConfirmPassword ? 'visibility_off' : 'visibility' }}
                      </span>
                    </button>
                  </div>
                  <div v-if="fieldErrors.confirmPassword" class="invalid-feedback tw-block tw-mt-1">
                    {{ fieldErrors.confirmPassword }}
                  </div>
                </div>

                <!-- Button -->
                <div class="tw-pt-2">
                  <button class="btn-register tw-w-full" type="submit" :disabled="isLoading || !isFormValid">
                    <span>{{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}</span>
                    <span v-if="isLoading" class="tw-inline-block tw-h-4 tw-w-4 tw-animate-spin tw-rounded-full tw-border-2 tw-border-current tw-border-t-transparent tw-ml-2" role="status"></span>
                    <span v-else class="material-symbols-outlined notranslate tw-ml-1" style="font-size: 18px;">
                      arrow_forward
                    </span>
                  </button>
                </div>
              </form>

              <footer class="form-footer tw-mt-4">
                <p class="reg-subtitle tw-mb-0">
                  ¿Ya tienes cuenta?
                  <a href="#" @click.prevent="router.push({ name: 'login' })">Inicia sesión</a>
                </p>
              </footer>
            </div>

            <!-- Success State -->
            <div v-else id="success-state" class="success-card tw-text-center tw-py-4 tw-px-3">
              <div class="success-icon-badge tw-mx-auto tw-mb-4">
                <span class="material-symbols-outlined notranslate success-icon">
                  check_circle
                </span>
              </div>

              <h2 class="reg-title tw-mb-2">¡Registro Exitoso!</h2>
              <p class="reg-subtitle tw-mx-auto tw-mb-4" style="max-width: 22rem;">
                Tu cuenta ha sido creada con éxito. Ya puedes iniciar sesión con tus credenciales.
              </p>

              <div class="tw-flex tw-flex-col tw-gap-2 tw-w-full tw-mx-auto" style="max-width: 320px;">
                <button class="btn-register tw-w-full" @click="router.push({ name: 'login' })">
                  <span>Ir a Iniciar Sesión</span>
                  <span class="material-symbols-outlined notranslate tw-text-xl">arrow_forward</span>
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import AuthRegisterSidebar from '@/modules/auth/components/AuthRegisterSidebar.vue';
import AuthRegisterMobileHeader from '@/modules/auth/components/AuthRegisterMobileHeader.vue';

const router = useRouter();
const authStore = useAuthStore();

// Form data
const firstName = ref('');
const lastName = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

// Errors State
const fieldErrors = reactive({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// UI states
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isLoading = ref(false);
const registrationSuccess = ref(false);
const errorMessage = ref('');

// Password strength properties
const strength = ref(0);
const strengthText = ref('Sin evaluar');
const strengthColor = ref('var(--outline-variant, #9e9e9e)');

const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

// --- Validaciones por Campo ---
const validateFirstName = (): boolean => {
  if (!firstName.value.trim()) {
    fieldErrors.firstName = 'El nombre es obligatorio.';
    return false;
  }
  if (firstName.value.trim().length < 2) {
    fieldErrors.firstName = 'El nombre debe tener al menos 2 caracteres.';
    return false;
  }
  fieldErrors.firstName = '';
  return true;
};

const validateLastName = (): boolean => {
  if (!lastName.value.trim()) {
    fieldErrors.lastName = 'El apellido es obligatorio.';
    return false;
  }
  if (lastName.value.trim().length < 2) {
    fieldErrors.lastName = 'El apellido debe tener al menos 2 caracteres.';
    return false;
  }
  fieldErrors.lastName = '';
  return true;
};

const validateUsername = (): boolean => {
  const usernameRegex = /^[a-zA-Z0-9_]{3,20}$/;
  if (!username.value.trim()) {
    fieldErrors.username = 'El nombre de usuario es obligatorio.';
    return false;
  }
  if (!usernameRegex.test(username.value.trim())) {
    fieldErrors.username = 'Entre 3 y 20 caracteres (solo letras, números y guion bajo).';
    return false;
  }
  fieldErrors.username = '';
  return true;
};

const validateEmail = (): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email.value.trim()) {
    fieldErrors.email = 'El correo electrónico es obligatorio.';
    return false;
  }
  if (!emailRegex.test(email.value.trim())) {
    fieldErrors.email = 'Introduce un correo electrónico válido.';
    return false;
  }
  fieldErrors.email = '';
  return true;
};

const validatePassword = (): boolean => {
  if (!password.value) {
    fieldErrors.password = 'La contraseña es obligatoria.';
    return false;
  }
  if (password.value.length < 8) {
    fieldErrors.password = 'Debe tener al menos 8 caracteres.';
    return false;
  }
  fieldErrors.password = '';
  return true;
};

const validateConfirmPassword = (): boolean => {
  if (!confirmPassword.value) {
    fieldErrors.confirmPassword = 'Debes confirmar la contraseña.';
    return false;
  }
  if (confirmPassword.value !== password.value) {
    fieldErrors.confirmPassword = 'Las contraseñas no coinciden.';
    return false;
  }
  fieldErrors.confirmPassword = '';
  return true;
};

// --- Cálculo de Fuerza de Contraseña ---
const checkStrength = (pwd: string) => {
  if (!pwd) {
    strength.value = 0;
    strengthText.value = 'Sin evaluar';
    strengthColor.value = 'var(--outline-variant, #9e9e9e)';
    return;
  }

  let score = 0;
  if (pwd.length >= 8) score += 25;
  if (/[A-Z]/.test(pwd)) score += 25;
  if (/[0-9]/.test(pwd)) score += 25;
  if (/[^A-Za-z0-9]/.test(pwd)) score += 25;

  strength.value = score;

  if (score <= 25) {
    strengthText.value = 'Débil';
    strengthColor.value = 'var(--error, #dc3545)';
  } else if (score <= 75) {
    strengthText.value = 'Media';
    strengthColor.value = 'var(--secondary, #ffc107)';
  } else {
    strengthText.value = 'Fuerte';
    strengthColor.value = '#22c55e';
  }
};

const onPasswordInput = () => {
  fieldErrors.password = '';
  checkStrength(password.value);
  if (confirmPassword.value) {
    validateConfirmPassword();
  }
};

const onConfirmPasswordInput = () => {
  fieldErrors.confirmPassword = '';
  if (confirmPassword.value === password.value) {
    fieldErrors.confirmPassword = '';
  }
};

// --- Validación Global del Formulario ---
const validateAllFields = (): boolean => {
  const isFirstValid = validateFirstName();
  const isLastValid = validateLastName();
  const isUsernameValid = validateUsername();
  const isEmailValid = validateEmail();
  const isPasswordValid = validatePassword();
  const isConfirmValid = validateConfirmPassword();

  return isFirstValid && isLastValid && isUsernameValid && isEmailValid && isPasswordValid && isConfirmValid;
};

const isFormValid = computed(() => {
  return (
    firstName.value.trim().length >= 2 &&
    lastName.value.trim().length >= 2 &&
    /^[a-zA-Z0-9_]{3,20}$/.test(username.value.trim()) &&
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim()) &&
    password.value.length >= 8 &&
    confirmPassword.value === password.value &&
    !Object.values(fieldErrors).some((err) => err !== '')
  );
});

// --- Registro ---
const handleRegistration = async () => {
  errorMessage.value = '';

  if (!validateAllFields()) {
    return;
  }

  isLoading.value = true;

  try {
    await authStore.register({
      first_name: firstName.value.trim(),
      last_name: lastName.value.trim(),
      username: username.value.trim(),
      email: email.value.trim(),
      password: password.value
    });

    registrationSuccess.value = true;
  } catch (error: any) {
    errorMessage.value =
      error.response?.data?.message ||
      error.response?.data?.error ||
      'Error al conectar con el servidor';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Mantén tus estilos exactamente como están */
:global(:root) {
  --outline: #76777d;
  --surface-container: #eceef0;
  --on-surface: #191c1e;
  --secondary-container: #645efb;
  --surface-container-low: #f2f4f6;
  --background: #f7f9fb;
  --outline-variant: #c6c6cd;
  --surface-container-lowest: #ffffff;
  --secondary: #4b41e1;
  --error: #ba1a1a;
  --on-surface-variant: #45464d;
  --surface-container-highest: #e0e3e5;
  --surface-dim: #d8dadc;
  --primary: #000000;
  --on-primary: #ffffff;
}

:global(html),
:global(body) {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
  background-color: var(--background);
  color: var(--on-surface);
}

.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;
}

.registration-wrapper {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
}

.bg-blobs {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.blob-a {
  position: absolute;
  top: -20%;
  left: -10%;
  width: 60%;
  height: 60%;
  border-radius: 50%;
  background: rgba(0, 0, 0, .05);
  filter: blur(120px);
}

.blob-b {
  position: absolute;
  bottom: -20%;
  right: -10%;
  width: 50%;
  height: 50%;
  border-radius: 50%;
  background: rgba(75, 65, 225, .05);
  filter: blur(120px);
}

.main-wrap {
  position: relative;
  z-index: 10;
  height: 100vh;
}

.form-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  height: 100vh;
  overflow-y: auto;
}

.form-section::-webkit-scrollbar {
  width: 6px;
}

.form-section::-webkit-scrollbar-thumb {
  background-color: var(--outline-variant);
  border-radius: 10px;
}

.form-section::-webkit-scrollbar-track {
  background: transparent;
}

.form-container {
  margin: auto 0;
}

@media(min-width: 768px) {
  .form-section {
    padding: 32px;
  }
}

@media(min-width: 992px) {
  .form-section {
    padding: 48px 32px;
  }
}

.reg-title {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -.01em;
  color: var(--primary);
}

@media(min-width: 768px) {
  .reg-title {
    font-size: 32px;
    letter-spacing: -.015em;
  }
}

.reg-subtitle {
  color: var(--on-surface-variant);
}

.form-label-custom {
  font-size: 14px;
  font-weight: 500;
  color: var(--on-surface);
}

.input-icon-wrap {
  position: relative;
}

.icon-left {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--outline-variant);
  pointer-events: none;
}

.toggle-icon {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--outline-variant);
  cursor: pointer;
}

.toggle-icon:hover {
  color: var(--primary);
}

.form-control-custom {
  height: 48px;
  padding-left: 48px;
  padding-right: 16px;
  background-color: var(--surface-container-lowest);
  border: 1px solid var(--outline-variant);
  border-radius: .75rem;
  font-size: 16px;
}

.form-control-custom.has-toggle {
  padding-right: 48px;
}

.form-control-custom:focus {
  outline: none;
  border-color: var(--secondary);
  box-shadow: 0 0 0 4px rgba(75, 65, 225, .10);
}

.form-control-custom.is-invalid {
  border-color: var(--app-error);
}

.form-control-custom.is-valid {
  border-color: var(--app-success);
}

.invalid-feedback {
  color: var(--app-error);
  font-size: 0.75rem;
}

.strength-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: .25rem;
}

.strength-text {
  font-size: 12px;
  color: var(--on-surface-variant);
}

.strength-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: .05em;
}

.strength-track {
  width: 100%;
  height: 4px;
  background-color: var(--surface-container-highest);
  border-radius: 9999px;
  overflow: hidden;
}

.password-strength-bar {
  height: 4px;
  border-radius: 9999px;
  transition: .3s ease;
}

.btn-register {
  width: 100%;
  height: 48px;
  background-color: var(--primary);
  color: var(--on-primary);
  font-size: 14px;
  font-weight: 700;
  border-radius: .75rem;
  border: none;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: .5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, .12);
}

.btn-register:hover {
  opacity: .9;
}

.btn-register:active {
  transform: scale(.98);
}

.form-footer {
  padding-top: 1.5rem;
  margin-top: 1rem;
  text-align: center;
  border-top: 1px solid rgba(198, 198, 205, .3);
}

.form-footer a {
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}

.success-icon {
  font-size: 64px;
  color: #22c55e;
}
</style>
