<template>
  <div class="af-support-card">
    <div class="af-support-icon-badge">
      <span class="material-symbols-outlined notranslate">support_agent</span>
    </div>
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

/* ============================================================
   Paleta "PROJECTHUB" — navy #10192B + dorado #C9974A
   Se apoya en las variables globales --ph-navy / --ph-gold ya
   definidas en :root (ver Login.vue / Register.vue).
   ============================================================ */

.af-support-card {
  /* Mismo navy que el sidebar de auth y los botones primarios del dashboard */
  background-color: var(--ph-navy, #10192B);
  color: #fff;
  padding: 24px;
  border-radius: 0.75rem;
  box-shadow: 0px 10px 30px rgba(16, 25, 43, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.04);
}

/* Ícono insignia en dorado, como acento de marca */
.af-support-icon-badge {
  width: 40px;
  height: 40px;
  border-radius: 0.65rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--ph-gold-soft, rgba(201, 151, 74, 0.16));
  color: var(--ph-gold, #C9974A);
  margin-bottom: 0.85rem;
}

.af-support-title {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.af-support-desc {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 1.5rem;
}

/* Botón en dorado sólido, como CTA de acento sobre el fondo navy */
.af-support-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background-color: var(--ph-gold, #C9974A);
  color: var(--ph-navy, #10192B);
  text-decoration: none;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-size: 14px;
  font-weight: 600;
  transition: background-color .15s ease;
}

.af-support-btn:hover {
  background-color: #d9ab5e;
  color: var(--ph-navy, #10192B);
}
</style>
