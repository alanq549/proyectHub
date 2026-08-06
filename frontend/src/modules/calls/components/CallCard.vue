<template>
  <div class="bg-white/70 dark:bg-slate-900/70 backdrop-blur-md border border-slate-200/80 dark:border-slate-800 rounded-3xl p-5 md:p-6 shadow-sm hover:shadow-md hover:border-slate-300 dark:hover:border-slate-700 transition-all duration-200 flex flex-col justify-between">
    <div>
      <!-- Encabezado de la Tarjeta (Título y Badge de Estado) -->
      <div class="flex items-start justify-between gap-3 mb-3">
        <h3 class="text-base font-bold text-slate-900 dark:text-white line-clamp-1 leading-snug">
          {{ call.title }}
        </h3>
        <span 
          :class="[
            'px-2.5 py-1 text-[11px] font-semibold rounded-full shrink-0 inline-flex items-center gap-1.5 transition-colors',
            call.is_active 
              ? 'bg-emerald-500/10 text-emerald-600 dark:bg-emerald-500/20 dark:text-emerald-400 border border-emerald-500/20' 
              : 'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400 border border-slate-200/60 dark:border-slate-700/60'
          ]"
        >
          <span class="relative flex h-2 w-2">
            <span v-if="call.is_active" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex rounded-full h-2 w-2" :class="call.is_active ? 'bg-emerald-500' : 'bg-slate-400'"></span>
          </span>
          {{ call.is_active ? 'Activa' : 'Inactiva' }}
        </span>
      </div>

      <!-- Descripción -->
      <p class="text-slate-600 dark:text-slate-400 text-xs mb-4 line-clamp-2 min-h-[32px] leading-relaxed">
        {{ call.description || 'Sin descripción disponible.' }}
      </p>

      <!-- Fechas de la Convocatoria -->
      <div class="border-t border-slate-100 dark:border-slate-800/80 pt-3.5 flex flex-col gap-2 text-xs text-slate-500 dark:text-slate-400 mb-4 bg-slate-50/50 dark:bg-slate-800/30 -mx-5 md:-mx-6 px-5 md:px-6 py-2.5">
        <div class="flex justify-between items-center">
          <span class="text-slate-400 dark:text-slate-500 flex items-center gap-1">
            <span class="material-symbols-outlined notranslate text-sm">calendar_today</span>
            Inicio:
          </span>
          <span class="font-semibold text-slate-700 dark:text-slate-200">{{ formatDate(call.start_date) }}</span>
        </div>
        <div class="flex justify-between items-center">
          <span class="text-slate-400 dark:text-slate-500 flex items-center gap-1">
            <span class="material-symbols-outlined notranslate text-sm">event_busy</span>
            Cierre:
          </span>
          <span class="font-semibold text-slate-700 dark:text-slate-200">{{ formatDate(call.end_date) }}</span>
        </div>
      </div>
    </div>

    <!-- Botones de Acción (Admin) -->
    <div v-if="isAdmin" class="flex items-center justify-end gap-2 border-t border-slate-100 dark:border-slate-800 pt-3">
      <button 
        @click="$emit('edit', call)" 
        class="text-xs font-semibold px-3 py-1.5 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 rounded-xl transition-all duration-150 inline-flex items-center gap-1 active:scale-95"
      >
        <span class="material-symbols-outlined notranslate text-base">edit</span>
        Editar
      </button>
      <button 
        @click="$emit('delete', call.id)" 
        class="text-xs font-semibold px-3 py-1.5 text-rose-600 dark:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-950/40 rounded-xl transition-all duration-150 inline-flex items-center gap-1 active:scale-95"
      >
        <span class="material-symbols-outlined notranslate text-base">delete</span>
        Eliminar
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Call } from '../services/callService'

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