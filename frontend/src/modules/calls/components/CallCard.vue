<template>
  <AppCard hoverable variant="glass" padding="md" class="tw-flex tw-flex-col tw-justify-between tw-h-full">
    <div>
      <div class="tw-flex tw-items-start tw-justify-between tw-gap-3 tw-mb-3">
        <h3 class="tw-text-base tw-font-bold tw-text-on-surface tw-line-clamp-1 tw-leading-snug">
          {{ call.title }}
        </h3>
        <AppBadge :variant="call.is_active ? 'success' : 'neutral'" :dot="true">
          {{ call.is_active ? 'Activa' : 'Inactiva' }}
        </AppBadge>
      </div>

      <p class="tw-text-on-surface-variant tw-text-xs tw-mb-4 tw-line-clamp-2 tw-min-h-[32px] tw-leading-relaxed">
        {{ call.description || 'Sin descripción disponible.' }}
      </p>

      <div class="tw-border-t tw-border-outline-variant tw-pt-3.5 tw-flex tw-flex-col tw-gap-2 tw-text-xs tw-text-on-surface-variant tw-mb-4 tw-bg-surface-container-low -tw-mx-5 md:-tw-mx-6 tw-px-5 md:tw-px-6 tw-py-2.5">
        <div class="tw-flex tw-justify-between tw-items-center">
          <span class="tw-text-outline tw-flex tw-items-center tw-gap-1">
            <span class="material-symbols-outlined notranslate tw-text-sm">calendar_today</span>
            Inicio:
          </span>
          <span class="tw-font-semibold tw-text-on-surface">{{ formatDate(call.start_date) }}</span>
        </div>
        <div class="tw-flex tw-justify-between tw-items-center">
          <span class="tw-text-outline tw-flex tw-items-center tw-gap-1">
            <span class="material-symbols-outlined notranslate tw-text-sm">event_busy</span>
            Cierre:
          </span>
          <span class="tw-font-semibold tw-text-on-surface">{{ formatDate(call.end_date) }}</span>
        </div>
      </div>
    </div>

    <div v-if="isAdmin" class="tw-flex tw-items-center tw-justify-end tw-gap-2 tw-border-t tw-border-outline-variant tw-pt-3">
      <AppButton variant="ghost" size="sm" icon="edit" @click="$emit('edit', call)">Editar</AppButton>
      <AppButton variant="danger" size="sm" icon="delete" @click="$emit('delete', call.id)">Eliminar</AppButton>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import type { Call } from '../services/callService'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'
import AppButton from '@/shared/components/AppButton.vue'

defineProps<{
  call: Call
  isAdmin?: boolean
}>()

defineEmits<{
  (e: 'edit', call: Call): void
  (e: 'delete', id: number): void
}>()

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>