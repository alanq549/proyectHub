<template>
  <div class="af-panel-card">
    <h3 class="af-section-title mb-3 d-flex align-items-center gap-2">
      <span class="material-symbols-outlined notranslate" style="color:#c2410c;">cloud_upload</span>
      Subir a S3
    </h3>
    <div class="af-dropzone" @click="$emit('browse')">
      <div class="af-dropzone-icon">
        <span class="material-symbols-outlined notranslate" style="font-size:40px; color: var(--af-secondary, #4b41e1);">file_upload</span>
      </div>
      <div class="text-center">
        <p class="af-dropzone-title mb-1">Arrastra tus archivos aquí</p>
        <p class="af-dropzone-sub mb-0">Soporta ZIP, PDF y RAW (Máx 50GB)</p>
      </div>
      <button class="af-link-btn bold underline">o busca en tu equipo</button>
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

.af-panel-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 24px;
  border-radius: 0.75rem;
  border: 1px solid rgba(198, 198, 205, 0.3);
  box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.04), 0px 2px 4px rgba(0, 0, 0, 0.02);
}
.af-section-title { font-size: 20px; font-weight: 600; color: var(--af-primary, #000); }

.af-dropzone {
  border: 2px dashed rgba(198,198,205,0.5);
  border-radius: 0.75rem;
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  background-color: rgba(242,244,246,0.3);
  cursor: pointer;
  transition: background-color .15s ease;
}
.af-dropzone:hover { background-color: rgba(242,244,246,0.6); }
.af-dropzone-icon {
  width: 64px; height: 64px;
  border-radius: 50%;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  transition: transform .2s ease;
}
.af-dropzone:hover .af-dropzone-icon { transform: scale(1.1); }
.af-dropzone-title { font-size: 14px; color: var(--af-primary, #000); font-weight: 700; }
.af-dropzone-sub { font-size: 12px; color: var(--af-on-surface-variant, #45464d); }
.af-link-btn {
  background: none;
  border: none;
  color: var(--af-secondary, #4b41e1);
  font-size: 14px;
}
.af-link-btn:hover { text-decoration: underline; }
.af-link-btn.bold { font-weight: 700; }
.af-link-btn.underline { text-decoration: underline; }
</style>
