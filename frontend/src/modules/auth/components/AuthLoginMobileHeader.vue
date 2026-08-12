<template>
  <!-- HEADER MOBILE -->
  <div class="tw-flex md:tw-hidden tw-justify-between tw-items-center tw-mb-5">
    <span class="brand-name">
      ProjectHub
    </span>
    <button class="btn-back-home" @click="router.push({ name: 'home' })">
      <span class="material-symbols-outlined notranslate">
        arrow_back
      </span>
      Inicio
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
const router = useRouter();
</script>

<style scoped>
.btn-back-home {
  border: none;
  background: transparent;
  color: var(--app-accent-melon, #B8863B);
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: .35rem;
  padding: 0;
}

.btn-back-home:hover {
  text-decoration: underline;
}

.brand-name {
  color: var(--app-primary, #1B2E44);
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
</style>
