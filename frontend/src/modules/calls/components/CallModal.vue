<template>
  <div
  v-if="isOpen"
  class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-sm p-4 transition-all">
    <div
      class="bg-white/90 dark:bg-slate-900/90 backdrop-blur-md rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200/80 dark:border-slate-800 transition-all">

      <!-- Header del Modal -->
      <div class="flex items-center gap-3 mb-5 pb-3 border-b border-slate-100 dark:border-slate-800">
        <div
          class="w-10 h-10 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-200 flex items-center justify-center shrink-0 border border-slate-200/60 dark:border-slate-700/50">
          <span class="material-symbols-outlined notranslate text-xl">
            campaign
          </span>
        </div>
        <h2 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">
          {{ isEditing ? 'Editar Convocatoria' : 'Nueva Convocatoria' }}
        </h2>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- Título -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Título <span class="text-rose-500">*</span>
          </label>
          <div
            class="flex rounded-2xl border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900 overflow-hidden focus-within:ring-2 focus-within:ring-slate-400/20 focus-within:border-slate-800 dark:focus-within:border-slate-400 transition-all">
            <span
              class="flex items-center justify-center px-3 bg-slate-50 dark:bg-slate-800/50 border-r border-slate-200 dark:border-slate-700/80 text-slate-400">
              <span class="material-symbols-outlined notranslate text-lg">title</span>
            </span>
            <input v-model="form.title" type="text" required placeholder="Ej. Convocatoria de Residencias 2026"
              class="w-full px-3 py-2 text-xs bg-transparent text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none" />
          </div>
        </div>

        <!-- Descripción -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Descripción</label>
          <textarea v-model="form.description" rows="3" placeholder="Detalles sobre los requisitos o alcance..."
            class="w-full px-3.5 py-2.5 text-xs bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 placeholder-slate-400 rounded-2xl border border-slate-200 dark:border-slate-700/80 focus:outline-none focus:ring-2 focus:ring-slate-400/20 focus:border-slate-800 dark:focus:border-slate-400 transition-all resize-none"></textarea>
        </div>

        <!-- Fechas (Grid) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Fecha Inicio <span class="text-rose-500">*</span>
            </label>
            <input v-model="form.start_date" type="datetime-local" required
              class="w-full px-3 py-2 text-xs bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-2xl border border-slate-200 dark:border-slate-700/80 focus:outline-none focus:ring-2 focus:ring-slate-400/20 focus:border-slate-800 dark:focus:border-slate-400 transition-all" />
          </div>
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">
              Fecha Fin <span class="text-rose-500">*</span>
            </label>
            <input v-model="form.end_date" type="datetime-local" required
              class="w-full px-3 py-2 text-xs bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-2xl border border-slate-200 dark:border-slate-700/80 focus:outline-none focus:ring-2 focus:ring-slate-400/20 focus:border-slate-800 dark:focus:border-slate-400 transition-all" />
          </div>
        </div>

        <!-- Checkbox Activo -->
        <div class="flex items-center gap-3 py-1">
          <input v-model="form.is_active" type="checkbox" id="is_active_call"
            class="w-4 h-4 rounded-md border-slate-300 dark:border-slate-700 text-slate-900 focus:ring-slate-400/20 dark:bg-slate-900 transition-colors cursor-pointer" />
          <label for="is_active_call"
            class="text-xs font-medium text-slate-700 dark:text-slate-300 cursor-pointer select-none">
            Convocatoria Activa
          </label>
        </div>

        <!-- Banner de Error -->
        <div v-if="errorMsg"
          class="flex items-center gap-2 py-2 px-3 text-xs rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20">
          <span class="material-symbols-outlined notranslate text-base shrink-0">error</span>
          <span class="font-medium">{{ errorMsg }}</span>
        </div>

        <!-- Acciones del Formulario -->
        <div class="flex justify-end gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
          <button type="button" @click="$emit('close')"
            class="px-4 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-2xl transition-all border border-slate-200 dark:border-slate-700/80 bg-white dark:bg-slate-900">
            Cancelar
          </button>

          <button type="submit" :disabled="loading"
            class="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-white bg-[#0F172A] hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white rounded-2xl transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed shadow-[0_4px_12px_rgba(15,23,42,0.15)] hover:-translate-y-0.5 active:translate-y-0">
            <svg v-if="loading" class="animate-spin h-4 w-4 text-white dark:text-slate-900" xmlns="http://www.w3.org/2000/svg" fill="none"
              viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
              </path>
            </svg>
            <span class="material-symbols-outlined notranslate text-base" v-else>save</span>
            <span>{{ loading ? 'Guardando...' : 'Guardar' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Call, CreateCallPayload } from '../services/callService'

const props = defineProps<{
  isOpen: boolean
  callToEdit?: Call | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'save', payload: CreateCallPayload): void
}>()

const isEditing = ref(false)
const loading = ref(false)
const errorMsg = ref('')

const form = ref({
  title: '',
  description: '',
  start_date: '',
  end_date: '',
  is_active: true
})

const toLocalDatetime = (isoStr: string) => {
  if (!isoStr) return ''
  const date = new Date(isoStr)
  const offset = date.getTimezoneOffset() * 60000
  return new Date(date.getTime() - offset).toISOString().slice(0, 16)
}

watch(() => props.callToEdit, (newVal) => {
  if (newVal) {
    isEditing.value = true
    form.value = {
      title: newVal.title,
      description: newVal.description || '',
      start_date: toLocalDatetime(newVal.start_date),
      end_date: toLocalDatetime(newVal.end_date),
      is_active: newVal.is_active
    }
  } else {
    isEditing.value = false
    form.value = { title: '', description: '', start_date: '', end_date: '', is_active: true }
  }
}, { immediate: true })

const handleSubmit = () => {
  errorMsg.value = ''
  if (new Date(form.value.end_date) < new Date(form.value.start_date)) {
    errorMsg.value = 'La fecha de fin debe ser posterior a la fecha de inicio.'
    return
  }

  emit('save', {
    title: form.value.title,
    description: form.value.description,
    start_date: new Date(form.value.start_date).toISOString(),
    end_date: new Date(form.value.end_date).toISOString(),
    is_active: form.value.is_active
  })
}
</script>