<template>
  <!--
    DashboardS3UploadPanel — Bloque 1.6a (Migración Bootstrap → Tailwind)
    • .form-select (Bootstrap) → form-select (plugin @tailwindcss/forms).
    • 8 utilidades Bootstrap migradas (mb-*, d-flex, gap, text-center).
    • .app-card-glass GLOBAL mantiene glassmorphism uniforme.
    • Acentos navy + dorado "PROJECTHUB" coherentes con el resto del dashboard.
  -->
  <AppCard variant="glass" class=" af-panel-card">
    <h3 class="af-section-title tw-mb-3 tw-flex tw-items-center tw-gap-2">
      <span class="material-symbols-outlined notranslate" style="color: var(--ph-gold, #C9974A);">cloud_upload</span>
      Subir archivos a S3
    </h3>

    <div class="tw-mb-3">
      <!-- @tailwindcss/forms strategy:"class" → clase form-select.
           Sobreescribe estilos con af-select local (tokens --app-input-*). -->
      <select class="form-select af-select" aria-label="Proyecto S3">
        <option selected>Proyecto archivos a S3</option>
      </select>
    </div>

    <div class="af-dropzone" @click="$emit('browse')">
      <div class="tw-text-center">
        <p class="af-dropzone-title tw-mb-1">Subir archivos a S3</p>
        <p class="af-dropzone-sub tw-mb-3">Con proyectos son dropzones</p>
      </div>
      <button class="af-btn-upload">
        <span class="material-symbols-outlined notranslate" style="font-size:18px;">upload</span>
        Subir archivo
      </button>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import AppCard from '@/shared/components/AppCard.vue'

defineEmits<{
  (event: 'browse'): void
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

/*
  El contenedor principal ya recibe glassmorphism + padding
  de la clase GLOBAL .app-card-glass. Sin definiciones locales duplicadas.
*/
.af-panel-card {
  /* Espacio específico S3 upload: si se necesita override futuro aquí */
}

.af-section-title {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: 16px;
  font-weight: 700;
  color: var(--ph-navy, #10192B);
}

.af-select {
  font-size: 13px;
  border-radius: var(--app-input-radius, 0.5rem);
  border: 1px solid var(--app-input-border, #e2e8f0);
  background-color: var(--app-input-bg, #ffffff);
}

.af-select:focus {
  outline: none;
  border-color: var(--ph-gold, #C9974A);
  box-shadow: 0 0 0 3px var(--ph-gold-soft, rgba(201, 151, 74, 0.12));
}

.af-dropzone {
  border: 2px dashed rgba(201, 151, 74, 0.35);
  border-radius: var(--app-glass-radius-sm, 0.75rem);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--ph-gold-soft, rgba(201, 151, 74, 0.05));
  cursor: pointer;
  transition: background-color .15s ease, border-color .15s ease;
}

.af-dropzone:hover {
  background-color: rgba(201, 151, 74, 0.1);
  border-color: rgba(201, 151, 74, 0.55);
}

.af-dropzone-title {
  font-size: 14px;
  color: var(--ph-navy, #10192B);
  font-weight: 700;
}

.af-dropzone-sub {
  font-size: 12px;
  color: var(--app-slate-500, #64748b);
}

/* Botón principal — navy, coherente con el resto del dashboard */
.af-btn-upload {
  background-color: var(--ph-navy, #10192B);
  color: #ffffff;
  border: none;
  padding: 0.45rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  box-shadow: 0 4px 12px rgba(16, 25, 43, 0.25);
  transition: background-color .15s ease;
  cursor: pointer;
}

.af-btn-upload:hover {
  background-color: var(--ph-navy-soft, #16233b);
}
</style>
