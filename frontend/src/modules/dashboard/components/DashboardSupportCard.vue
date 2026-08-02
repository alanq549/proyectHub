<template>
  <div class="af-support-card">
    <h4 class="af-support-title">Soporte Técnico</h4>
    <p class="af-support-desc">¿Necesitas ayuda con la configuración de S3 o permisos de usuario?</p>
    <a href="#" class="af-support-btn" @click.prevent="$emit('contact')">
      <span class="material-symbols-outlined notranslate">support_agent</span>
      Contactar Soporte
    </a>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  (event: 'contact'): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

.af-support-card {
  background-color: var(--af-primary-container, #131b2e);
  color: #fff;
  padding: 24px;
  border-radius: 0.75rem;
  box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.04), 0px 2px 4px rgba(0, 0, 0, 0.02);
}
.af-support-title { font-size: 20px; font-weight: 600; margin-bottom: 0.5rem; }
.af-support-desc { font-size: 12px; color: #7c839b; margin-bottom: 1.5rem; }
.af-support-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background-color: rgba(255,255,255,0.1);
  color: #fff;
  text-decoration: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 14px;
  transition: background-color .15s ease;
}
.af-support-btn:hover { background-color: rgba(255,255,255,0.2); color: #fff; }
</style>
