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
    <AppCard variant="glass" padding="none">
      <div v-if="loading" class="tw-p-8 tw-text-center">
        <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-primary">
          progress_activity
        </span>
      </div>

      <div v-else-if="submissions.length === 0" class="tw-p-8 tw-text-center tw-text-on-surface-variant">
        No hay proyectos registrados aún en esta convocatoria.
      </div>

      <table v-else class="tw-w-full tw-text-left tw-text-sm">
        <thead class="tw-bg-surface-container-low tw-border-b tw-border-outline-variant">
          <tr>
            <th class="tw-py-3 tw-px-4">Proyecto</th>
            <th class="tw-py-3 tw-px-4">Participante / Equipo</th>
            <th class="tw-py-3 tw-px-4">Estado</th>
            <th class="tw-py-3 tw-px-4 tw-text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="tw-divide-y tw-divide-outline-variant/40">
          <tr v-for="item in submissions" :key="item.id" class="hover:tw-bg-surface-container-lowest">
            <td class="tw-py-3 tw-px-4 tw-font-semibold">{{ item.title }}</td>
            <td class="tw-py-3 tw-px-4">{{ item.user_email || item.author_name }}</td>
            <td class="tw-py-3 tw-px-4">
              <AppBadge :variant="getStatusVariant(item.status)">
                {{ item.status }}
              </AppBadge>
            </td>
            <td class="tw-py-3 tw-px-4 tw-text-right">
              <button 
                @click="openReviewModal(item)"
                class="tw-px-3 tw-py-1.5 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-xs tw-font-medium"
              >
                Revisar y Dar Seguimiento
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </AppCard>

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