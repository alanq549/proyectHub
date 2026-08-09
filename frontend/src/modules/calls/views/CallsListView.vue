//src/modules/calls/views/CallsListView.vue
<template>
  <div class="tw-py-2 tw-max-w-7xl tw-mx-auto tw-space-y-6">
    <div class="tw-flex tw-flex-col sm:tw-flex-row tw-justify-between tw-items-start sm:tw-items-center tw-gap-4">
      <div>
        <h1 class="tw-text-2xl tw-font-bold tw-text-on-surface tw-tracking-tight">Convocatorias</h1>
        <p class="tw-text-on-surface-variant tw-text-xs tw-mt-1">Control centralizado de fechas, estados y recepción de
          proyectos.</p>
      </div>

      <AppButton v-if="isAdmin" variant="primary" icon="campaign" @click="openModalForCreate">
        Nueva Convocatoria
      </AppButton>
    </div>

    <div class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 lg:tw-grid-cols-4 tw-gap-4">
      <AppCard variant="glass" class="tw-flex tw-items-center tw-justify-between">
        <div>
          <span class="tw-text-xs tw-font-medium tw-text-outline tw-block tw-mb-1">Total Convocatorias</span>
          <span class="tw-text-2xl tw-font-bold tw-text-on-surface">{{ calls.length }}</span>
        </div>
        <div
          class="tw-w-10 tw-h-10 tw-rounded-2xl tw-bg-surface-container tw-text-on-surface-variant tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-xl">campaign</span>
        </div>
      </AppCard>

      <AppCard variant="glass" class="tw-flex tw-items-center tw-justify-between">
        <div>
          <span class="tw-text-xs tw-font-medium tw-text-outline tw-block tw-mb-1">Convocatorias Activas</span>
          <span class="tw-text-2xl tw-font-bold tw-text-on-surface">{{calls.filter(c => c.is_active).length}}</span>
        </div>
        <div
          class="tw-w-10 tw-h-10 tw-rounded-2xl tw-bg-success-bg tw-text-success tw-flex tw-items-center tw-justify-center tw-shrink-0">
          <span class="material-symbols-outlined notranslate tw-text-xl">check_circle</span>
        </div>
      </AppCard>
    </div>

    <div v-if="loading" class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-20 tw-gap-3">
      <svg class="tw-animate-spin tw-h-8 tw-w-8 tw-text-primary" xmlns="http://www.w3.org/2000/svg" fill="none"
        viewBox="0 0 24 24">
        <circle class="tw-opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="tw-opacity-75" fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
        </path>
      </svg>
      <span class="tw-text-xs tw-text-on-surface-variant tw-font-medium">Cargando convocatorias...</span>
    </div>

    <AppCard v-else-if="calls.length === 0" variant="glass"
      class="tw-text-center tw-py-16 tw-px-4 tw-border-dashed tw-flex tw-flex-col tw-items-center tw-justify-center">
      <div
        class="tw-w-12 tw-h-12 tw-rounded-2xl tw-bg-surface-container tw-text-outline tw-flex tw-items-center tw-justify-center tw-mb-3">
        <span class="material-symbols-outlined notranslate tw-text-2xl">campaign</span>
      </div>
      <h3 class="tw-text-sm tw-font-bold tw-text-on-surface">No hay convocatorias registradas</h3>
      <p class="tw-text-on-surface-variant tw-text-xs tw-mt-1 tw-max-w-xs">
        {{ isAdmin ? 'Crea una nueva convocatoria para comenzar a publicar fechas.' : 'Por el momento no existen convocatorias activas.' }}
      </p>
      <AppButton v-if="isAdmin" variant="primary" icon="add" class="tw-mt-4" @click="openModalForCreate">
        Crear la primera
      </AppButton>
    </AppCard>

    <div v-else class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
      <CallCard v-for="call in calls" :key="call.id" :call="call" :is-admin="isAdmin" @edit="openModalForEdit"
        @delete="handleDelete" />
    </div>

    <CallModal :is-open="isModalOpen" :call-to-edit="selectedCall" @close="isModalOpen = false" @save="handleSave" />
  </div>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import type { Call, CreateCallPayload } from '../services/callService'
import { useAuthStore } from '@/stores/authStore'

import { useCallStore } from '../stores/callStore'

import CallCard from '../components/CallCard.vue'
import CallModal from '../components/CallModal.vue'
import AppCard from '@/shared/components/AppCard.vue'
import AppButton from '@/shared/components/AppButton.vue'


const authStore = useAuthStore()

const isAdmin = computed(() =>
  authStore.user?.role === 'admin'
)


const callStore = useCallStore()


// Datos provenientes del store (cache)
const { calls, loading } = storeToRefs(callStore)


const isModalOpen = ref(false)

const selectedCall = ref<Call | null>(null)



onMounted(() => {
  callStore.fetchCalls()
})



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

      await callStore.updateCall(
        selectedCall.value.id,
        payload
      )

    } else {

      await callStore.createCall(payload)

    }


    isModalOpen.value = false


  } catch (err) {

    console.error(
      'Error al guardar convocatoria:',
      err
    )

  }

}



const handleDelete = async (id: number) => {

  if (confirm('¿Estás seguro de eliminar esta convocatoria?')) {

    try {

      await callStore.deleteCall(id)

    } catch (err) {

      console.error(
        'Error al eliminar convocatoria:',
        err
      )

    }

  }

}

</script>
