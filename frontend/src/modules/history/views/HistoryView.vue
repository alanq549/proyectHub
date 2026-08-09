<template>
  <section class="tw-space-y-6">
    <div>
      <div class="tw-mb-1 tw-flex tw-items-center tw-gap-2">
        <span class="material-symbols-outlined notranslate tw-text-primary">history</span>
        <h2 class="tw-text-xl tw-font-bold tw-text-on-surface">
          {{ isAdmin ? 'Auditoría General del Sistema' : 'Mi Historial de Actividad' }}
        </h2>
      </div>
      <p class="tw-text-sm tw-text-on-surface-variant">
        {{ 
          isAdmin 
            ? 'Registro global de acciones realizadas por todos los usuarios en la plataforma.' 
            : 'Registro de tus acciones recientes dentro de la plataforma.' 
        }}
      </p>
    </div>

    <!-- Indicador de carga -->
    <div v-if="loading" class="tw-flex tw-justify-center tw-py-8">
      <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-primary">progress_activity</span>
    </div>

    <!-- Contenido Principal -->
    <AppCard v-else padding="md" variant="flat">
      <div v-if="logs.length === 0" class="tw-text-center tw-py-8">
        <span class="material-symbols-outlined notranslate tw-text-3xl tw-text-outline tw-mb-2">event_busy</span>
        <p class="tw-text-sm tw-text-on-surface-variant">No hay registros de actividad disponibles.</p>
      </div>

      <div v-else class="tw-overflow-x-auto">
        <table class="tw-w-full tw-text-left tw-border-collapse">
          <thead>
            <tr class="tw-border-b tw-border-outline-variant tw-text-xs tw-font-semibold tw-text-on-surface-variant">
              <th class="tw-pb-3 tw-px-3" v-if="isAdmin">Usuario ID</th>
              <th class="tw-pb-3 tw-px-3">Acción</th>
              <th class="tw-pb-3 tw-px-3">Entidad</th>
              <th class="tw-pb-3 tw-px-3">Detalles</th>
              <th class="tw-pb-3 tw-px-3">Fecha</th>
            </tr>
          </thead>
          <tbody class="tw-divide-y tw-divide-outline-variant tw-text-sm tw-text-on-surface">
            <tr v-for="log in logs" :key="log.id" class="hover:tw-bg-surface-container/50 tw-transition-colors">
              <td v-if="isAdmin" class="tw-py-3 tw-px-3 tw-font-mono tw-text-xs">{{ log.user_id }}</td>
              <td class="tw-py-3 tw-px-3">
                <AppBadge variant="secondary">{{ log.action }}</AppBadge>
              </td>
              <td class="tw-py-3 tw-px-3">
                <span v-if="log.entity_type" class="tw-text-xs tw-font-medium tw-bg-surface-container tw-px-2 tw-py-1 tw-rounded">
                  {{ log.entity_type }} #{{ log.entity_id }}
                </span>
                <span v-else class="tw-text-xs tw-text-on-surface-variant">N/A</span>
              </td>
              <td class="tw-py-3 tw-px-3 tw-text-on-surface-variant tw-max-w-xs tw-truncate">
                {{ log.description || 'Sin detalles adicionales' }}
              </td>
              <td class="tw-py-3 tw-px-3 tw-text-xs tw-text-on-surface-variant">
                {{ new Date(log.created_at).toLocaleString() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </AppCard>
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { historyService, type ActivityLogModel } from '../services/historyService'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const logs = ref<ActivityLogModel[]>([])
const loading = ref(true)

const isAdmin = computed(() => authStore.user?.role === 'admin')

async function fetchHistory() {
  try {
    loading.value = true
    logs.value = await historyService.getHistory({ limit: 50 })
  } catch (err) {
    console.error('Error al cargar el historial:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchHistory()
})
</script>