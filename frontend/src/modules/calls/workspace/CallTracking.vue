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
  <div class="bg-white p-6 rounded-xl border border-gray-100 shadow-sm space-y-6">
    <h3 class="text-lg font-bold text-gray-800">Línea de Tiempo del Proyecto</h3>
    
    <div class="relative border-l border-gray-200 ml-4 space-y-6">
      <div v-for="item in tracking" :key="item.id" class="mb-6 ml-6">
        <span class="absolute -left-3 flex items-center justify-center w-6 h-6 bg-indigo-100 rounded-full ring-8 ring-white">
          <span class="material-symbols-outlined text-indigo-600 text-sm">history</span>
        </span>
        <div class="bg-gray-50 p-4 rounded-lg border border-gray-100">
          <div class="flex justify-between items-center mb-1">
            <span class="font-semibold text-gray-800 capitalize">{{ item.action }}</span>
            <time class="text-xs text-gray-400">{{ new Date(item.created_at).toLocaleString() }}</time>
          </div>
          <p class="text-sm text-gray-600">{{ item.description || 'Sin descripción' }}</p>
        </div>
      </div>

      <div v-if="tracking?.length === 0" class="text-gray-400 text-sm py-4 ml-2">
        No hay registros de actividad aún.
      </div>
    </div>
  </div>
</template>