<!-- src/modules/calls/components/CallCard.vue -->
<template>
  <AppCard 
    hoverable 
    variant="glass" 
    padding="md"
    class="tw-flex tw-flex-col tw-h-full tw-transition-all hover:tw-shadow-lg hover:-tw-translate-y-0.5 tw-cursor-pointer" 
    @click="handleCardClick"
  >
    <!-- 1. ENCABEZADO -->
    <div class="tw-flex tw-items-center tw-justify-between tw-mb-4">
      <div class="tw-inline-flex tw-items-center tw-gap-1.5 tw-px-3 tw-py-1 tw-rounded-full tw-bg-primary/10 tw-text-primary tw-text-xs tw-font-semibold">
        <span class="material-symbols-outlined notranslate tw-text-sm">campaign</span>
        Convocatoria
      </div>

      <AppBadge :variant="call.is_active ? 'success' : 'neutral'" :dot="true">
        {{ call.is_active ? 'Abierta' : 'Cerrada' }}
      </AppBadge>
    </div>

    <!-- 2. TÍTULO Y DESCRIPCIÓN -->
    <h2 class="tw-text-lg tw-font-bold tw-leading-snug tw-text-on-surface tw-mb-2">
      {{ call.title }}
    </h2>

    <p class="tw-text-sm tw-text-on-surface-variant tw-line-clamp-3 tw-leading-relaxed tw-flex-1">
      {{ call.description || 'Consulta los requisitos y participa en esta convocatoria.' }}
    </p>

    <!-- 3. VIGENCIA -->
    <div class="tw-mt-5 tw-rounded-xl tw-bg-surface-container-low tw-p-3.5 tw-border tw-border-outline-variant/40">
      <div class="tw-flex tw-items-center tw-gap-1.5 tw-text-xs tw-text-outline tw-mb-2.5 tw-font-medium">
        <span class="material-symbols-outlined notranslate tw-text-base">schedule</span>
        Vigencia
      </div>

      <div class="tw-flex tw-items-center tw-justify-between tw-text-xs">
        <div>
          <div class="tw-text-outline">Inicio</div>
          <div class="tw-font-semibold tw-text-on-surface tw-mt-0.5">
            {{ formatDate(call.start_date) }}
          </div>
        </div>
        <span class="material-symbols-outlined notranslate tw-text-outline tw-text-sm">east</span>
        <div class="tw-text-right">
          <div class="tw-text-outline">Cierre</div>
          <div class="tw-font-semibold tw-text-on-surface tw-mt-0.5">
            {{ formatDate(call.end_date) }}
          </div>
        </div>
      </div>
    </div>

    <!-- 4. SECCIÓN ESPECÍFICA DE USUARIO -->
    <template v-if="!isAdmin">
      <div class="tw-flex tw-items-center tw-justify-between tw-border-t tw-border-outline-variant/60 tw-pt-4 tw-mt-5 group-hover:tw-text-primary">
        <span class="tw-text-sm tw-font-semibold tw-text-primary">
          Entrar al espacio de trabajo
        </span>
        <span class="material-symbols-outlined notranslate tw-text-primary tw-transition-transform hover:tw-translate-x-1">
          arrow_forward
        </span>
      </div>
    </template>

    <!-- 5. SECCIÓN ESPECÍFICA DE ADMINISTRADOR -->
    <template v-else>
      <div class="tw-flex tw-items-center tw-justify-between tw-border-t tw-border-outline-variant/60 tw-pt-3.5 tw-mt-5">
        <div class="tw-flex tw-items-center tw-gap-1.5 tw-text-outline tw-text-xs tw-font-semibold">
          <span class="material-symbols-outlined notranslate tw-text-sm">admin_panel_settings</span>
          Gestión Admin
        </div>

        <div class="tw-flex tw-gap-2">
          <AppButton variant="ghost" size="sm" icon="settings" @click.stop="handleCardClick">
            Administrar
          </AppButton>
          <AppButton variant="danger" size="sm" icon="delete" @click.stop="$emit('delete', props.call.id)">
            Eliminar
          </AppButton>
        </div>
      </div>
    </template>
  </AppCard>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Call } from '../services/callService'
import AppBadge from '@/shared/components/AppBadge.vue'
import AppButton from '@/shared/components/AppButton.vue'
import AppCard from '@/shared/components/AppCard.vue'

const router = useRouter()

const props = defineProps<{
  call: Call
  isAdmin?: boolean
}>()

defineEmits<{
  (e: 'edit', call: Call): void
  (e: 'delete', id: number): void
}>()

function handleCardClick() {
  // Redirigir a la vista del Workspace tanto para Admin como para Usuario
  router.push({
    name: 'call-information',
    params: { id: props.call.id }
  })
}

function formatDate(dateStr: string) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('es-MX', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}
</script>