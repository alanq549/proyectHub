<!-- src/modules/calls/workspace/CallTracking.vue -->
<script setup lang="ts">
import type { ActivityLogModel } from '@/modules/history/services/historyService'

interface Props {
  tracking?: ActivityLogModel[];
}

withDefaults(defineProps<Props>(), {
  tracking: () => []
})
</script>

<template>
  <section class="app-card-glass tw-p-8 tw-space-y-6">
    <!-- ENCABEZADO -->
    <div class="tw-flex tw-items-center tw-gap-3">
      <div
        class="tw-w-10 tw-h-10 tw-rounded-xl tw-bg-[var(--app-surface-container)] tw-text-[var(--app-primary)] tw-flex tw-items-center tw-justify-center tw-shrink-0">
        <span class="material-symbols-outlined notranslate tw-text-xl">history</span>
      </div>
      <div>
        <h3 class="tw-font-bold tw-text-lg tw-text-[var(--app-ink-900)]">Línea de tiempo del proyecto</h3>
        <p class="tw-text-xs tw-text-[var(--app-slate-500)]">Registro cronológico de actividades y eventos clave.</p>
      </div>
    </div>

    <!-- LÍNEA DE TIEMPO -->
    <div class="tw-relative tw-border-l tw-border-[var(--app-outline-variant)] tw-ml-4 tw-space-y-6 tw-py-2">
      <div v-for="item in tracking" :key="item.id" class="tw-relative tw-ml-6">
        <!-- Indicador de punto en la línea -->
        <span
          class="tw-absolute -tw-left-[31px] tw-flex tw-items-center tw-justify-center tw-w-6 h-6 tw-h-6 tw-rounded-full tw-bg-[var(--app-surface-container-high)] tw-border tw-border-[var(--app-outline-variant)] tw-text-[var(--app-primary)] tw-shadow-sm">
          <span class="material-symbols-outlined notranslate tw-text-xs">radio_button_checked</span>
        </span>

        <!-- Tarjeta de Actividad -->
        <div
          class="tw-p-4 tw-rounded-xl tw-bg-[var(--app-surface-container-low)] tw-border tw-border-[var(--app-outline-variant)] tw-transition-all hover:tw-border-[var(--app-primary-light)] hover:tw-shadow-sm">
          <div class="tw-flex tw-flex-col sm:tw-flex-row sm:tw-justify-between sm:tw-items-center tw-gap-1 tw-mb-2">
            <span class="tw-font-bold tw-text-sm tw-text-[var(--app-ink-800)] tw-capitalize">
              {{ item.action }}
            </span>
            <time
              class="tw-font-mono tw-text-xs tw-text-[var(--app-slate-400)] tw-bg-[var(--app-surface)] tw-px-2.5 tw-py-0.5 tw-rounded-md tw-border tw-border-[var(--app-outline-variant)]">
              {{ new Date(item.created_at).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' }) }}
            </time>
          </div>
          <p class="tw-text-sm tw-text-[var(--app-slate-600)] tw-leading-relaxed">
            {{ item.description || 'Sin descripción disponible.' }}
          </p>
        </div>
      </div>

      <!-- ESTADO VACÍO -->
      <div v-if="tracking?.length === 0"
        class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-12 tw-px-4 tw-rounded-xl tw-bg-[var(--app-surface-container-low)] tw-border tw-border-dashed tw-border-[var(--app-outline-variant)]">
        <span
          class="material-symbols-outlined notranslate tw-text-3xl tw-text-[var(--app-slate-400)] tw-mb-2">event_note</span>
        <p class="tw-text-sm tw-font-medium tw-text-[var(--app-ink-800)]">Sin registros de actividad</p>
        <p class="tw-text-xs tw-text-[var(--app-slate-500)] tw-mt-0.5">Las acciones del proyecto aparecerán aquí
          conforme avancen.</p>
      </div>
    </div>
  </section>
</template>