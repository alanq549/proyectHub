<template>
  <div v-if="isOpen" class="tw-fixed tw-inset-0 tw-z-50 tw-flex tw-items-center tw-justify-center tw-bg-black/40 tw-backdrop-blur-sm tw-p-4 tw-transition-all">
    <AppCard variant="glass" padding="lg" class="tw-max-w-md tw-w-full">
      <template #header>
        <div class="tw-flex tw-items-center tw-gap-3">
          <div class="tw-w-10 tw-h-10 tw-rounded-2xl tw-bg-surface-container tw-text-on-surface-variant tw-flex tw-items-center tw-justify-center tw-shrink-0 tw-border tw-border-outline-variant">
            <span class="material-symbols-outlined notranslate tw-text-xl">campaign</span>
          </div>
          <h2 class="tw-text-lg tw-font-bold tw-text-on-surface tw-leading-tight">
            {{ isEditing ? 'Editar Convocatoria' : 'Nueva Convocatoria' }}
          </h2>
        </div>
      </template>

      <form @submit.prevent="handleSubmit" class="tw-space-y-4">
        <div>
          <label class="tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant tw-mb-1">
            Título <span class="tw-text-error">*</span>
          </label>
          <AppInput v-model="form.title" icon="title" placeholder="Ej. Convocatoria de Residencias 2026" />
        </div>

        <div>
          <label class="tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant tw-mb-1">Descripción</label>
          <textarea v-model="form.description" rows="3" placeholder="Detalles sobre los requisitos o alcance..." class="tw-w-full tw-px-3.5 tw-py-2.5 tw-text-sm tw-bg-surface-container-lowest tw-text-on-surface placeholder:tw-text-outline tw-rounded-xl tw-border tw-border-outline-variant focus:tw-outline-none focus:tw-border-primary focus:tw-ring-1 focus:tw-ring-primary tw-transition-all tw-resize-none"></textarea>
        </div>

        <div class="tw-grid tw-grid-cols-1 sm:tw-grid-cols-2 tw-gap-4">
          <div>
            <label class="tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant tw-mb-1">
              Fecha Inicio <span class="tw-text-error">*</span>
            </label>
            <input v-model="form.start_date" type="datetime-local" required class="tw-w-full tw-px-3 tw-py-2 tw-text-sm tw-bg-surface-container-lowest tw-text-on-surface tw-rounded-xl tw-border tw-border-outline-variant focus:tw-outline-none focus:tw-border-primary focus:tw-ring-1 focus:tw-ring-primary tw-transition-all" />
          </div>
          <div>
            <label class="tw-block tw-text-xs tw-font-semibold tw-text-on-surface-variant tw-mb-1">
              Fecha Fin <span class="tw-text-error">*</span>
            </label>
            <input v-model="form.end_date" type="datetime-local" required class="tw-w-full tw-px-3 tw-py-2 tw-text-sm tw-bg-surface-container-lowest tw-text-on-surface tw-rounded-xl tw-border tw-border-outline-variant focus:tw-outline-none focus:tw-border-primary focus:tw-ring-1 focus:tw-ring-primary tw-transition-all" />
          </div>
        </div>

        <div class="tw-flex tw-items-center tw-gap-3 tw-py-1">
          <input v-model="form.is_active" type="checkbox" id="is_active_call" class="tw-w-4 tw-h-4 tw-rounded-md tw-border-outline-variant tw-text-primary focus:tw-ring-primary/20 tw-transition-colors tw-cursor-pointer" />
          <label for="is_active_call" class="tw-text-xs tw-font-medium tw-text-on-surface-variant tw-cursor-pointer tw-select-none">
            Convocatoria Activa
          </label>
        </div>

        <div v-if="errorMsg" class="tw-flex tw-items-center tw-gap-2 tw-py-2 tw-px-3 tw-text-xs tw-rounded-xl tw-bg-error-bg tw-text-error tw-border tw-border-error/20">
          <span class="material-symbols-outlined notranslate tw-text-base tw-shrink-0">error</span>
          <span class="tw-font-medium">{{ errorMsg }}</span>
        </div>

        <div class="tw-flex tw-justify-end tw-gap-3 tw-pt-4 tw-border-t tw-border-outline-variant tw-mt-4">
          <AppButton type="button" variant="secondary" @click="$emit('close')">Cancelar</AppButton>
          <AppButton type="submit" variant="primary" :loading="loading" icon="save">Guardar</AppButton>
        </div>
      </form>
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Call, CreateCallPayload } from '../services/callService'
import AppCard from '@/shared/components/AppCard.vue'
import AppInput from '@/shared/components/AppInput.vue'
import AppButton from '@/shared/components/AppButton.vue'

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