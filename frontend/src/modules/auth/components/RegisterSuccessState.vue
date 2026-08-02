<template>
  <!-- Success State -->
  <div id="success-state" class="show">
    <div class="success-icon-wrap">
      <span class="material-symbols-outlined notranslate" style="font-size:48px; font-variation-settings: 'FILL' 1;">check_circle</span>
    </div>
    <h2 class="reg-title">¡Registro Exitoso!</h2>
    <p class="reg-subtitle mx-auto" style="max-width: 20rem;">Hemos enviado un enlace de verificación a tu
      correo electrónico. Por favor, revisa tu bandeja de entrada para activar tu cuenta.</p>
    <button class="btn-back-home" @click="onReloadPage()">
      Volver al inicio
    </button>
  </div>
</template>

<script setup lang="ts">


const props = defineProps<{
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

.success-icon-wrap {
  width: 80px;
  height: 80px;
  background-color: rgba(75, 65, 225, 0.10);
  color: var(--secondary, #4b41e1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.btn-back-home {
  padding: 0 2rem;
  height: 48px;
  background-color: var(--surface-container-highest, #e0e3e5);
  color: var(--primary, #000000);
  font-size: 14px;
  font-weight: 700;
  border-radius: 0.75rem;
  border: none;
  transition: background-color .15s ease;
}

.btn-back-home:hover {
  background-color: var(--surface-dim, #d8dadc);
}

.reg-title {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.01em;
  color: var(--primary, #000000);
}

@media (min-width: 768px) {
  .reg-title {
    font-size: 32px;
    letter-spacing: -0.015em;
  }
}

.reg-subtitle {
  color: var(--on-surface-variant, #45464d);
}
</style>