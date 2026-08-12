<template>
  <!-- Success State -->
  <div id="success-state" class="show">
    <div class="success-icon-wrap">
      <span class="material-symbols-outlined notranslate" style="font-size:48px; font-variation-settings: 'FILL' 1;">check_circle</span>
    </div>
    <h2 class="reg-title">¡Registro exitoso!</h2>
    <p class="reg-subtitle tw-mx-auto" style="max-width: 20rem;">Hemos enviado un enlace de verificación a tu
      correo electrónico. Por favor, revisa tu bandeja de entrada para activar tu cuenta.</p>
    <button class="btn-back-home" @click="onReloadPage()">
      Volver al inicio
    </button>
  </div>
</template>

<script setup lang="ts">

const { onReloadPage } = defineProps<{
  onReloadPage: () => void;
}>();

</script>

<style scoped>
/* Success state */
/* #success-state{ display: none; } */
/* Controlled by v-if */
#success-state.show {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 24px;
  animation: fadeIn 0.5s ease forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Antes morado (#4b41e1); ahora latón, el mismo acento que ya
   usan los botones de énfasis en el resto del flujo. */
.success-icon-wrap {
  width: 80px;
  height: 80px;
  background-color: rgba(184, 134, 59, 0.12);
  color: var(--app-accent-melon, #B8863B);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.btn-back-home {
  padding: 0 2rem;
  height: 48px;
  background-color: var(--app-surface-container-highest, #DCE5EC);
  color: var(--app-primary, #1B2E44);
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  font-size: 14px;
  font-weight: 700;
  border-radius: 0.75rem;
  border: none;
  transition: background-color .15s ease, color .15s ease;
}

.btn-back-home:hover {
  background-color: var(--app-accent-melon-light, #E8D2A6);
  color: var(--app-ink-900, #14243A);
}

.reg-title {
  font-family: var(--app-font-display, 'Fraunces', serif);
  font-size: 26px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--app-primary, #1B2E44);
}

@media (min-width: 768px) {
  .reg-title {
    font-size: 34px;
    letter-spacing: -0.015em;
  }
}

.reg-subtitle {
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  color: var(--app-on-surface-variant, #4C6479);
  line-height: 1.6;
}
</style>
