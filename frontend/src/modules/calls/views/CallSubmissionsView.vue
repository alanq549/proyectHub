<!-- src/modules/calls/views/CallSubmissionsView.vue -->
<template>
  <section class="tw-space-y-6">
    <div class="tw-flex tw-items-center tw-justify-between">
      <div>
        <h2 class="tw-text-xl tw-font-bold tw-text-on-surface">Proyectos e Inscritos</h2>
        <p class="tw-text-sm tw-text-on-surface-variant">
          Seguimiento y evaluación de propuestas para {{ call.title }}.
        </p>
      </div>
    </div>

    <!-- Filtros y Estado Vacío / Tabla -->
    <div v-if="loading" class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-24 tw-gap-4">
      <div class="tw-w-16 tw-h-16 tw-rounded-2xl tw-bg-[var(--app-surface-container)] tw-flex tw-items-center tw-justify-center tw-shadow-sm">
        <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-3xl tw-text-[var(--app-primary)]">progress_activity</span>
      </div>
      <span class="tw-text-sm tw-text-[var(--app-on-surface-variant)] tw-font-medium tw-tracking-wide">Cargando proyectos...</span>
    </div>

    <AppCard v-else-if="submissions.length === 0" variant="glass"
      class="tw-text-center tw-py-16 tw-px-4 tw-border-dashed tw-flex tw-flex-col tw-items-center tw-justify-center tw-mt-4">
      <div
        class="tw-w-16 tw-h-16 tw-rounded-3xl tw-bg-[var(--app-surface-container)] tw-text-[var(--app-secondary)] tw-flex tw-items-center tw-justify-center tw-mb-4 tw-shadow-sm">
        <span class="material-symbols-outlined notranslate tw-text-3xl">folder_off</span>
      </div>
      <h3 class="tw-text-base tw-font-bold tw-text-[var(--app-primary)]">Sin proyectos registrados</h3>
      <p class="tw-text-[var(--app-on-surface-variant)] tw-text-sm tw-mt-2 tw-max-w-md">
        Aún no hay propuestas enviadas para esta convocatoria. Los participantes inscritos aparecerán aquí.
      </p>
    </AppCard>

    <div v-else class="app-card-glass-table tw-w-full tw-overflow-x-auto tw-mt-4">
      <table class="tw-w-full tw-text-left tw-text-sm">
        <thead class="tw-bg-[var(--app-surface-container-low)] tw-border-b tw-border-[var(--app-outline-variant)]">
          <tr>
            <th class="tw-py-4 tw-px-6 tw-font-semibold tw-text-[var(--app-primary)]">Proyecto</th>
            <th class="tw-py-4 tw-px-6 tw-font-semibold tw-text-[var(--app-primary)]">Participante / Equipo</th>
            <th class="tw-py-4 tw-px-6 tw-font-semibold tw-text-[var(--app-primary)]">Estado</th>
            <th class="tw-py-4 tw-px-6 tw-text-right tw-font-semibold tw-text-[var(--app-primary)]">Acciones</th>
          </tr>
        </thead>
        <tbody class="tw-divide-y tw-divide-[var(--app-outline-variant)]/40">
          <tr v-for="item in submissions" :key="item.id" class="hover:tw-bg-[var(--app-surface-container-lowest)] tw-transition-colors">
            <td class="tw-py-4 tw-px-6 tw-font-medium tw-text-[var(--app-ink-800)]">{{ item.title }}</td>
            <td class="tw-py-4 tw-px-6 tw-text-[var(--app-slate-600)]">{{ item.user_email || item.author_name }}</td>
            <td class="tw-py-4 tw-px-6">
              <AppBadge :variant="getStatusVariant(item.status)">
                {{ item.status }}
              </AppBadge>
            </td>
            <td class="tw-py-4 tw-px-6 tw-text-right">
              <button 
                @click="openReviewModal(item)"
                class="app-btn-primary tw-inline-flex tw-items-center tw-justify-center tw-px-4 tw-text-xs tw-gap-2"
                style="height: 36px;"
              >
                Revisar 
                <span class="material-symbols-outlined tw-text-[16px]">arrow_forward</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal de Revisión -->
    <CallReviewModal 
      v-if="selectedProjectForReview" 
      :project="selectedProjectForReview" 
      @close="selectedProjectForReview = null"
      @updated="fetchSubmissions"
    />
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { Call } from '../services/callService'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'
import { projectService, type Project } from '@/modules/projects/services/projectService'
import CallReviewModal from '../components/CallReviewModal.vue'

const props = defineProps<{
  call: Call
}>()

const submissions = ref<Project[]>([])
const loading = ref(true)
const selectedProjectForReview = ref<Project | null>(null)

async function fetchSubmissions() {
  try {
    loading.value = true
    submissions.value = await projectService.getAll({ call_id: props.call.id })
  } catch (err) {
    console.error('Error al cargar inscritos:', err)
  } finally {
    loading.value = false
  }
}

function getStatusVariant(status?: string) {
  switch (status) {
    case 'approved': return 'success'
    case 'rejected': return 'error'
    case 'submitted': return 'warning'
    default: return 'neutral'
  }
}

function openReviewModal(item: Project) {
  selectedProjectForReview.value = item
}

onMounted(() => {
  fetchSubmissions()
})
</script>