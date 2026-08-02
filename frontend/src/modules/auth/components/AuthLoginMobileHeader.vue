<template>
  <!-- HEADER MOBILE -->
  <div class="d-md-none d-flex justify-content-between align-items-center mb-5">
    <span class="brand-name" style="color:var(--primary)">
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
  color: var(--secondary, #4b41e1);
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
  color: var(--primary, #000000);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
}
</style>