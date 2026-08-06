<template>
  <!--
    DashboardS3UploadPanel — Bloque 1.6a (Migración Bootstrap → Tailwind)
    • .form-select (Bootstrap) → form-select (plugin @tailwindcss/forms).
    • 8 utilidades Bootstrap migradas (mb-*, d-flex, gap, text-center).
    • .app-card-glass GLOBAL mantiene glassmorphism uniforme.
  -->
  <div class="app-card-glass af-panel-card">
    <h3 class="af-section-title mb-3 flex items-center gap-2">
      <span class="material-symbols-outlined notranslate" style="color: var(--app-primary, #4b41e1);">cloud_upload</span>
      Subir archivos a S3
    </h3>

    <div class="mb-3">
      <!-- @tailwindcss/forms strategy:"class" → clase form-select.
           Sobreescribe estilos con af-select local (tokens --app-input-*). -->
      <select class="form-select af-select" aria-label="Proyecto S3">
        <option selected>Proyecto archivos a S3</option>
      </select>
    </div>

    <div class="af-dropzone" @click="$emit('browse')">
      <div class="text-center">
        <p class="af-dropzone-title mb-1">Subir archivos a S3</p>
        <p class="af-dropzone-sub mb-3">Con proyectos son dropzones</p>
      </div>
      <button class="af-btn-upload">
        <span class="material-symbols-outlined notranslate" style="font-size:18px;">upload</span>
        Subir archivo
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  (event: 'browse'): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

/*
  El contenedor principal ya recibe glassmorphism + padding
  de la clase GLOBAL .app-card-glass. Sin definiciones locales duplicadas.
*/
.af-panel-card {
  /* Espacio específico S3 upload: si se necesita override futuro aquí */
}

.af-section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--app-black, #000);
}

.af-select {
  font-size: 13px;
  border-radius: var(--app-input-radius, 0.5rem);
  border: 1px solid var(--app-input-border, #e2e8f0);
  background-color: var(--app-input-bg, #ffffff);
}

.af-dropzone {
  border: 2px dashed rgba(75, 65, 225, 0.25);
  border-radius: var(--app-glass-radius-sm, 0.75rem);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(242, 244, 246, 0.4);
  cursor: pointer;
  transition: background-color .15s ease;
}

.af-dropzone:hover { background-color: rgba(75, 65, 225, 0.04); }

.af-dropzone-title {
  font-size: 14px;
  color: var(--app-black, #000);
  font-weight: 700;
}

.af-dropzone-sub {
  font-size: 12px;
  color: var(--app-slate-500, #64748b);
}

.af-btn-upload {
  background-color: var(--app-primary, #4b41e1);
  color: var(--app-on-primary, #fff);
  border: none;
  padding: 0.45rem 1.25rem;
  border-radius: 0.5rem;
  font-size: 13px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  box-shadow: 0 4px 12px rgba(75, 65, 225, 0.25);
  cursor: pointer;
}

.af-btn-upload:hover {
  background-color: var(--app-primary-dark, #4338ca);
}
</style>