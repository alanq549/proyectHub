<!-- src/modules/calls/workspace/WorkspaceHeader.vue -->
<script setup lang="ts">
import type { Call } from '../services/callService'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'

defineProps<{
  call: Call
}>()
</script>

<template>
  <AppCard variant="glass" class="tw-p-6">
    <div class="tw-flex tw-flex-col tw-gap-4 sm:tw-flex-row sm:tw-items-center sm:tw-justify-between">
      <!-- Info principal -->
      <div class="tw-flex tw-items-center tw-gap-4">
        <!-- Icono contenedor alineado a la guía (§8.10) -->
        <div class="tw-flex tw-h-12 tw-w-12 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-surface-container tw-text-primary">
          <span class="material-symbols-outlined notranslate tw-text-2xl">
            campaign
          </span>
        </div>

        <div>
          <!-- Título principal h1 (§4.1) -->
          <h1 class="tw-text-2xl tw-font-bold tw-text-on-surface">
            {{ call.title }}
          </h1>

          <!-- Texto secundario (§4.2) -->
          <p class="tw-text-sm tw-text-on-surface-variant">
            Convocatoria académica
          </p>
        </div>
      </div>

      <!-- Estado / Badge -->
      <div class="tw-flex tw-items-center">
        <AppBadge
          :variant="call.is_active ? 'success' : 'neutral'"
          :dot="true"
        >
          {{ call.is_active ? 'Abierta' : 'Cerrada' }}
        </AppBadge>
      </div>
    </div>
  </AppCard>
</template>