<!-- src/modules/calls/views/CallWorkspaceView.vue -->
<template>
  <div class="tw-py-2 tw-max-w-7xl tw-mx-auto tw-space-y-6">
    <!-- Cargando -->
    <div v-if="loading && !currentWorkspace" class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-24 tw-gap-4">
      <div class="tw-w-16 tw-h-16 tw-rounded-2xl tw-bg-[var(--app-surface-container)] tw-flex tw-items-center tw-justify-center tw-shadow-sm">
        <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-3xl tw-text-[var(--app-primary)]">progress_activity</span>
      </div>
      <span class="tw-text-sm tw-text-[var(--app-on-surface-variant)] tw-font-medium tw-tracking-wide">Configurando tu espacio de trabajo...</span>
    </div>

    <!-- Error -->
    <AppCard v-else-if="error && !currentWorkspace" variant="glass"
      class="tw-text-center tw-py-20 tw-px-4 tw-border-dashed tw-flex tw-flex-col tw-items-center tw-justify-center tw-max-w-2xl tw-mx-auto tw-mt-8">
      <div
        class="tw-w-16 tw-h-16 tw-rounded-3xl tw-bg-[var(--app-error-bg)] tw-text-[var(--app-error)] tw-flex tw-items-center tw-justify-center tw-mb-4 tw-shadow-sm">
        <span class="material-symbols-outlined notranslate tw-text-3xl">error</span>
      </div>
      <h3 class="tw-text-lg tw-font-bold tw-text-[var(--app-primary)]">No se pudo cargar la convocatoria</h3>
      <p class="tw-text-[var(--app-on-surface-variant)] tw-text-sm tw-mt-2 tw-max-w-md">
        {{ error }}
      </p>
    </AppCard>

    <!-- Workspace Unificado -->
    <template v-else-if="call && currentWorkspace">
      <!-- Header con las pestañas integradas dentro de la tarjeta -->
      <WorkspaceHeader :call="call" :workspace="currentWorkspace" />

      <!-- Vistas de las pestañas -->
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

<script setup lang="ts">
import { computed, onMounted, watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'

import WorkspaceHeader from '../workspace/WorkspaceHeader.vue'
import { useWorkspaceStore } from '../stores/workspaceStore'
import { historyService, type ActivityLogModel } from '@/modules/history/services/historyService'
import AppCard from '@/shared/components/AppCard.vue'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

const { currentWorkspace, loading, error } = storeToRefs(workspaceStore)

const call = computed(() => currentWorkspace.value?.call ?? null)

const trackingLogs = ref<ActivityLogModel[]>([])
const loadingHistory = ref(false)

async function fetchProjectHistory(projectId: number) {
  if (!projectId) return
  loadingHistory.value = true
  try {
    trackingLogs.value = historyService.getHistory ? await historyService.getHistory({
      entity_type: 'Project',
      entity_id: projectId,
      limit: 50
    }) : []
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