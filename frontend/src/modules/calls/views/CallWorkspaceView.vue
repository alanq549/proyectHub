<!-- src/modules/calls/views/CallWorkspaceView.vue -->
<script setup lang="ts">
import { computed, onMounted, watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'

import WorkspaceHeader from '../workspace/WorkspaceHeader.vue'
import WorkspaceTabs from '../workspace/WorkspaceTabs.vue'
import { useWorkspaceStore } from '../stores/workspaceStore'
import { historyService, type ActivityLogModel } from '@/modules/history/services/historyService'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

const { currentWorkspace, loading, error } = storeToRefs(workspaceStore)

const call = computed(() => currentWorkspace.value?.call ?? null)

// Variable reactiva para almacenar el historial de este proyecto
const trackingLogs = ref<ActivityLogModel[]>([])
const loadingHistory = ref(false)

// Función para cargar la línea de tiempo del proyecto asociado
async function fetchProjectHistory(projectId: number) {
  if (!projectId) return
  loadingHistory.value = true
  try {
    trackingLogs.value = await historyService.getHistory({
      entity_type: 'Project',
      entity_id: projectId,
      limit: 50
    })
  } catch (err) {
    console.error('Error al cargar la línea de tiempo:', err)
  } finally {
    loadingHistory.value = false
  }
}

async function loadData(forceRefresh = false) {
  const callId = Number(route.params.id)
  if (Number.isInteger(callId)) {
    await workspaceStore.fetchWorkspace(callId, forceRefresh)

    // Tipamos con 'unknown' en vez de 'any' y acotamos la forma esperada
    // antes de acceder a sus propiedades, para mantener la seguridad de tipos.
    const workspaceData = currentWorkspace.value as unknown as {
      project?: { id?: number }
      project_id?: number
    }
    const projectId = workspaceData?.project?.id || workspaceData?.project_id

    if (projectId) {
      await fetchProjectHistory(projectId)
    }
  }
}

onMounted(() => {
  loadData()
})

watch(
  () => route.params.id,
  () => {
    loadData()
  }
)
</script>

<template>
  <div class="tw-space-y-6">
    <!-- Cargando -->
    <div
      v-if="loading && !currentWorkspace"
      class="tw-flex tw-items-center tw-justify-center tw-py-16"
    >
      <div class="loading-state tw-flex tw-items-center tw-gap-3">
        <span class="material-symbols-outlined notranslate tw-animate-spin loading-icon">
          progress_activity
        </span>
        <span>Cargando espacio de trabajo...</span>
      </div>
    </div>

    <!-- Error -->
    <div
      v-else-if="error && !currentWorkspace"
      class="tw-rounded-xl tw-border tw-border-error/20 tw-bg-error/5 tw-p-6"
    >
      <div class="tw-flex tw-items-start tw-gap-3">
        <span class="material-symbols-outlined notranslate tw-text-error">
          error
        </span>
        <div>
          <h2 class="tw-font-semibold tw-text-on-surface">
            No se pudo cargar la convocatoria
          </h2>
          <p class="tw-mt-1 tw-text-sm tw-text-on-surface-variant">
            {{ error }}
          </p>
        </div>
      </div>
    </div>

    <!-- Workspace -->
    <template v-else-if="call && currentWorkspace">
      <WorkspaceHeader :call="call" />

      <!-- Renderizar pestañas según el estado -->
      <WorkspaceTabs :workspace="currentWorkspace" />

      <!-- Le inyectamos el historial a través de las props hacia las pestañas hijas / RouterView -->
      <RouterView v-slot="{ Component }">
        <component
          :is="Component"
          :call="call"
          :workspace="currentWorkspace"
          :tracking="trackingLogs"
        />
      </RouterView>
    </template>
  </div>
</template>

<style scoped>
/* ============================================================
   Acentos "PROJECTHUB" — misma paleta navy #10192B + dorado #C9974A
   usada en Login.vue, Register.vue, CallCard.vue y CallFormModal.vue.
   ============================================================ */

/* Estado de carga: texto navy, spinner dorado como color de acento */
.loading-state {
  color: var(--ph-navy, #10192B);
  font-weight: 500;
}

.loading-icon {
  color: var(--ph-gold, #C9974A);
}
</style>
