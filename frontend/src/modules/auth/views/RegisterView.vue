<template>
  <div class="registration-wrapper">
    <div class="bg-blobs">
      <div class="blob-a"></div>
      <div class="blob-b"></div>
    </div>

    <main class="main-wrap">
      <div class="row g-0 h-100">
        <AuthRegisterSidebar />

        <!-- Registration Section -->
        <div class="col-12 col-lg-7 form-section">
          <div class="w-100 form-container" style="max-width:480px;">
            <AuthRegisterMobileHeader />

            <!-- Register Form -->
            <div v-if="!registrationSuccess">
              <header class="mb-4">
                <h2 class="reg-title mb-2">Crear una cuenta</h2>
                <p class="reg-subtitle mb-0">
                  Ingresa tus datos para comenzar tu trayecto académico.
                </p>
              </header>

              <!-- Mensaje de error -->
              <div v-if="errorMessage" class="alert alert-danger py-2 small mb-3">
              {{ errorMessage }}
            </div>

              <form @submit.prevent="handleRegistration">
                <!-- Username -->
                <div class="mb-3">
                  <label class="form-label-custom">Nombre de usuario</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined icon-left">person</span>
                    <input v-model="username" type="text" class="form-control form-control-custom"
                      placeholder="ej. jdoe_research" required />
                  </div>
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label class="form-label-custom">Correo electrónico</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined icon-left">mail</span>
                    <input v-model="email" type="email" class="form-control form-control-custom"
                      placeholder="correo@universidad.edu" required />
                  </div>
                </div>

                <!-- Password -->
                <div class="mb-3">
                  <label class="form-label-custom">Contraseña</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined icon-left">lock</span>
                    <input v-model="password" :type="showPassword ? 'text' : 'password'"
                      class="form-control form-control-custom has-toggle" placeholder="••••••••" required
                      @input="checkStrength(password)" />
                    <button type="button" class="toggle-icon" @click="togglePassword">
                      <span class="material-symbols-outlined">
                        {{ showPassword ? 'visibility_off' : 'visibility' }}
                      </span>
                    </button>
                  </div>
                  <div class="pt-1">
                    <div class="strength-row">
                      <span class="strength-text">Seguridad de la contraseña</span>
                      <span class="strength-label" :style="{ color: strengthColor }">
                        {{ strengthText }}
                      </span>
                    </div>
                    <div class="strength-track">
                      <div class="password-strength-bar" :style="{
                        width: strength + '%',
                        backgroundColor: strengthColor
                      }"></div>
                    </div>
                  </div>
                </div>

                <!-- Confirm Password -->
                <div class="mb-3">
                  <label class="form-label-custom">Confirmar contraseña</label>
                  <div class="input-icon-wrap">
                    <span class="material-symbols-outlined icon-left">verified_user</span>
                    <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control form-control-custom has-toggle" placeholder="••••••••" required />
                    <button type="button" class="toggle-icon" @click="toggleConfirmPassword">
                      <span class="material-symbols-outlined">
                        {{ showConfirmPassword ? 'visibility_off' : 'visibility' }}
                      </span>
                    </button>
                  </div>
                </div>

                <!-- Button -->
                <div class="pt-2">
                  <button class="btn-register" type="submit" :disabled="isLoading">
                    <span>{{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}</span>
                    <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>
                    <span v-else class="material-symbols-outlined" style="font-size:18px;">
                      arrow_forward
                    </span>
                  </button>
                </div>
              </form>

              <footer class="form-footer">
                <p class="reg-subtitle mb-0">
                  ¿Ya tienes cuenta?
                  <a href="#" @click.prevent="router.push({ name: 'login' })">Inicia sesión</a>
                </p>
              </footer>
            </div>
           <!-- Success State -->
<div v-else id="success-state" class="success-card text-center py-4 px-3">
  <!-- Glowing Icon Wrapper -->
  <div class="success-icon-badge mx-auto mb-4">
    <span class="material-symbols-outlined success-icon">
      check_circle
    </span>
  </div>

  <!-- Content -->
  <h2 class="reg-title mb-2">¡Registro Exitoso!</h2>
  <p class="reg-subtitle mx-auto mb-4" style="max-width: 22rem;">
    Hemos enviado un enlace de verificación a tu correo. Por favor, revisa tu bandeja de entrada para activar tu cuenta.
  </p>

  <!-- Action Buttons -->
  <div class="d-flex flex-column gap-2 w-100 mx-auto" style="max-width: 320px;">
    <button class="btn-primary-custom w-100" @click="router.push({ name: 'login' })">
      <span>Ir a Iniciar Sesión</span>
      <span class="material-symbols-outlined fs-5">arrow_forward</span>
    </button>
    
    <button class="btn-ghost-custom w-100" @click="router.push({ name: 'home' })">
      Volver al inicio
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import AuthRegisterSidebar from '@/modules/auth/components/AuthRegisterSidebar.vue';
import AuthRegisterMobileHeader from '@/modules/auth/components/AuthRegisterMobileHeader.vue';

const router = useRouter();
const authStore = useAuthStore();

// Form data
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

// UI states
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const isLoading = ref(false);
const registrationSuccess = ref(false);
const errorMessage = ref('');

// Password strength
const strength = ref(0);
const strengthText = ref('Baja');
const strengthColor = ref('var(--outline-variant)');

// Toggle password visibility
const togglePassword = () => {
  showPassword.value = !showPassword.value;
};

const toggleConfirmPassword = () => {
  showConfirmPassword.value = !showConfirmPassword.value;
};

// Password security checker
const checkStrength = (pwd: string) => {
  if (!pwd.length) {
    strength.value = 0;
    strengthText.value = 'Baja';
    strengthColor.value = 'var(--outline-variant)';
    return;
  }

  let newStrength = 0;

  if (pwd.length > 5) newStrength += 25;
  if (pwd.length > 10) newStrength += 25;
  if (/[A-Z]/.test(pwd)) newStrength += 25;
  if (/[0-9]/.test(pwd)) newStrength += 25;

  if (newStrength <= 25) {
    strengthText.value = 'Débil';
    strengthColor.value = 'var(--error)';
  } else if (newStrength <= 75) {
    strengthText.value = 'Media';
    strengthColor.value = 'var(--secondary)';
  } else {
    strengthText.value = 'Fuerte';
    strengthColor.value = '#22c55e';
  }

  strength.value = newStrength;
};

// Petición Real al Backend Flask
const handleRegistration = async () => {
  errorMessage.value = '';

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Las contraseñas no coinciden';
    return;
  }

  isLoading.value = true;

  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value // Se enviará de manera segura por HTTPS
    });

    registrationSuccess.value = true;
  } catch (error: any) {
    errorMessage.value = error.response?.data?.message || 'Error al conectar con el servidor';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
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
  /* Evita el scroll global en la ventana */
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

/* Base Wrapper */
.registration-wrapper {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
}

/* Background */
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

/* Form Section con Scroll Interno Limpio */
.form-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 16px;
  height: 100vh;
  overflow-y: auto;
  /* Permite scroll local únicamente si la pantalla es muy pequeña */
}

/* Estilo moderno para el scrollbar en caso de ser necesario */
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
  /* Centra verticalmente el contenido dentro del contenedor scrollable */
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

/* Strength */
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

/* Button */
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

/* Footer */
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
</style>