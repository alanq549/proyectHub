<!-- src/modules/calls/components/CallRequirementsAdmin.vue -->
<template>
  <AppCard variant="glass" padding="md" class="tw-space-y-4">
    <div class="tw-flex tw-items-center tw-justify-between">
      <h3 class="tw-text-base tw-font-bold tw-text-on-surface">Requisitos de la Convocatoria</h3>
      <AppButton size="sm" variant="primary" icon="add" @click="showForm = !showForm">
        {{ showForm ? 'Cancelar' : 'Agregar Requisito' }}
      </AppButton>
    </div>

    <!-- Formulario rápido para añadir requisito -->
    <div v-if="showForm" class="tw-p-4 tw-rounded-xl tw-bg-surface-container-low tw-space-y-3 tw-border tw-border-outline-variant/40">
      <input 
        v-model="newReq.title" 
        placeholder="Título del requisito (ej. Formato PDF de Solicitud)"
        class="tw-w-full tw-px-3 tw-py-2 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
      />
      <textarea 
        v-model="newReq.description" 
        placeholder="Instrucciones o detalles opcionales"
        class="tw-w-full tw-px-3 tw-py-2 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
        rows="2"
      ></textarea>
      <div class="tw-flex tw-items-center tw-justify-between">
        <label class="tw-flex tw-items-center tw-gap-2 tw-text-xs tw-text-on-surface-variant">
          <input type="checkbox" v-model="newReq.is_required" /> Obligatorio
        </label>
        <AppButton size="sm" variant="primary" :disabled="!newReq.title" @click="saveRequirement">
          Guardar Requisito
        </AppButton>
      </div>
    </div>

    <!-- Lista de Requisitos Existentes -->
    <ul v-if="requirements.length > 0" class="tw-divide-y tw-divide-outline-variant/30">
      <li v-for="req in requirements" :key="req.id" class="tw-py-2.5 tw-flex tw-items-center tw-justify-between">
        <div>
          <span class="tw-text-sm tw-font-semibold tw-text-on-surface">{{ req.title }}</span>
          <p class="tw-text-xs tw-text-on-surface-variant">{{ req.description }}</p>
        </div>
        <AppBadge :variant="req.is_required ? 'error' : 'neutral'">
          {{ req.is_required ? 'Requerido' : 'Opcional' }}
        </AppBadge>
      </li>
    </ul>
    <p v-else class="tw-text-xs tw-text-outline tw-text-center tw-py-4">
      No se han configurado requisitos para esta convocatoria.
    </p>
  </AppCard>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { callService, type CallRequirement } from '../services/callService'
import AppCard from '@/shared/components/AppCard.vue'
import AppButton from '@/shared/components/AppButton.vue'
import AppBadge from '@/shared/components/AppBadge.vue'

const props = defineProps<{
  callId: number
}>()

const requirements = ref<CallRequirement[]>([])
const showForm = ref(false)
const newReq = ref({ title: '', description: '', is_required: true })

async function saveRequirement() {
  if (!newReq.value.title) return
  try {
    const created = await callService.addRequirement(props.callId, newReq.value)
    requirements.value.push(created)
    newReq.value = { title: '', description: '', is_required: true }
    showForm.value = false
  } catch (err) {
    console.error('Error al agregar requisito:', err)
  }
}
</script>