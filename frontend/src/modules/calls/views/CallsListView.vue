<template>
  <div class="py-2 max-w-7xl mx-auto space-y-6">
    
    <!-- Encabezado Limpio (Alineado exactamente con 'Gestión de Usuarios') -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900 dark:text-white tracking-tight">Convocatorias</h1>
        <p class="text-slate-500 dark:text-slate-400 text-xs mt-1">Control centralizado de fechas, estados y recepción de proyectos.</p>
      </div>

      <button 
        v-if="isAdmin" 
        @click="openModalForCreate" 
        class="inline-flex items-center gap-2 px-4 py-2.5 rounded-2xl text-xs font-semibold bg-[#0F172A] hover:bg-slate-800 text-white dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white transition-all duration-200 shadow-[0_4px_12px_rgba(15,23,42,0.15)] hover:-translate-y-0.5 active:translate-y-0 shrink-0"
      >
        <span class="material-symbols-outlined notranslate text-lg">campaign</span>
        <span>Nueva Convocatoria</span>
      </button>
    </div>

    <!-- Métrica Rápida / Resumen KPI (Coherente con los Cards Superiores de ProjectHub) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-5 rounded-3xl border border-slate-200/60 dark:border-slate-800 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-slate-400 dark:text-slate-500 block mb-1">Total Convocatorias</span>
          <span class="text-2xl font-bold text-slate-900 dark:text-white">{{ calls.length }}</span>
        </div>
        <div class="w-10 h-10 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 flex items-center justify-center shrink-0">
          <span class="material-symbols-outlined notranslate text-xl">campaign</span>
        </div>
      </div>

      <div class="bg-white/80 dark:bg-slate-900/80 backdrop-blur-md p-5 rounded-3xl border border-slate-200/60 dark:border-slate-800 shadow-sm flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-slate-400 dark:text-slate-500 block mb-1">Convocatorias Activas</span>
          <span class="text-2xl font-bold text-slate-900 dark:text-white">{{ calls.filter(c => c.is_active).length }}</span>
        </div>
        <div class="w-10 h-10 rounded-2xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
          <span class="material-symbols-outlined notranslate text-xl">check_circle</span>
        </div>
      </div>
    </div>

    <!-- Spinner Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 gap-3">
      <svg class="animate-spin h-8 w-8 text-slate-900 dark:text-slate-100" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="text-xs text-slate-400 dark:text-slate-500 font-medium">Cargando convocatorias...</span>
    </div>

    <!-- Estado Vacío (Estilo Dropzone Subir Archivos a S3) -->
    <div 
      v-else-if="calls.length === 0" 
      class="text-center py-16 px-4 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md rounded-3xl border border-dashed border-slate-200 dark:border-slate-800 shadow-sm flex flex-col items-center justify-center"
    >
      <div class="w-12 h-12 rounded-2xl bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 flex items-center justify-center mb-3">
        <span class="material-symbols-outlined notranslate text-2xl">campaign</span>
      </div>
      <h3 class="text-sm font-bold text-slate-900 dark:text-white">No hay convocatorias registradas</h3>
      <p class="text-slate-400 dark:text-slate-500 text-xs mt-1 max-w-xs">
        {{ isAdmin ? 'Crea una nueva convocatoria para comenzar a publicar fechas.' : 'Por el momento no existen convocatorias activas.' }}
      </p>
      <button 
        v-if="isAdmin" 
        @click="openModalForCreate" 
        class="mt-4 inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold bg-[#0F172A] text-white hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 rounded-2xl transition-all shadow-sm"
      >
        <span class="material-symbols-outlined notranslate text-base">add</span>
        Crear la primera
      </button>
    </div>

    <!-- Grid de Tarjetas -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <CallCard 
        v-for="call in calls" 
        :key="call.id" 
        :call="call" 
        :is-admin="isAdmin"
        @edit="openModalForEdit"
        @delete="handleDelete"
      />
    </div>

    <!-- Modal -->
    <CallModal 
      :is-open="isModalOpen" 
      :call-to-edit="selectedCall" 
      @close="isModalOpen = false" 
      @save="handleSave" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { callService, type Call, type CreateCallPayload } from '../services/callService'
import { useAuthStore } from '@/stores/authStore'
import CallCard from '../components/CallCard.vue'
import CallModal from '../components/CallModal.vue'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.user?.role === 'admin')

const calls = ref<Call[]>([])
const loading = ref(true)
const isModalOpen = ref(false)
const selectedCall = ref<Call | null>(null)

const fetchCalls = async () => {
  try {
    loading.value = true
    calls.value = await callService.getCalls()
  } catch (err) {
    console.error('Error al obtener convocatorias:', err)
  } finally {
    loading.value = false
  }
}

const openModalForCreate = () => {
  selectedCall.value = null
  isModalOpen.value = true
}

const openModalForEdit = (call: Call) => {
  selectedCall.value = call
  isModalOpen.value = true
}

const handleSave = async (payload: CreateCallPayload) => {
  try {
    if (selectedCall.value) {
      await callService.updateCall(selectedCall.value.id, payload)
    } else {
      await callService.createCall(payload)
    }
    isModalOpen.value = false
    await fetchCalls()
  } catch (err) {
    console.error('Error al guardar convocatoria:', err)
  }
}

const handleDelete = async (id: number) => {
  if (confirm('¿Estás seguro de eliminar esta convocatoria?')) {
    try {
      await callService.deleteCall(id)
      await fetchCalls()
    } catch (err) {
      console.error('Error al eliminar convocatoria:', err)
    }
  }
}

onMounted(() => {
  fetchCalls()
})
</script>