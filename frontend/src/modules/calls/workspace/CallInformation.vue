<!-- src/modules/calls/views/CallInformation.vue -->
<template>
  <section class="tw-space-y-8">
    <!-- ENCABEZADO: Uso de tipografía display para mayor impacto -->
    <div class="tw-flex tw-items-center tw-justify-between tw-flex-wrap tw-gap-4">
      <div class="tw-space-y-1">
        <h2 class="tw-text-3xl tw-font-semibold tw-text-[var(--app-primary)]">
          Información de la convocatoria
        </h2>
        <p class="tw-text-sm tw-text-[var(--app-slate-500)]">
          {{ isAdmin ? 'Gestiona los parámetros, fechas y requisitos.' : 'Consulta los detalles y condiciones de participación.' }}
        </p>
      </div>

      <!-- ACCIONES: Botón de acento (Latón) para el llamado principal -->
      <div class="tw-flex tw-gap-3">
        <template v-if="isAdmin">
          <AppButton v-if="!isEditing" variant="primary" icon="edit" @click="isEditing = true">
            Editar convocatoria
          </AppButton>
          <div v-else class="tw-flex tw-gap-2">
            <AppButton variant="secondary" @click="cancelEdit">Cancelar</AppButton>
            <AppButton variant="primary" :loading="saving" @click="saveChanges">Guardar cambios</AppButton>
          </div>
        </template>

        <button
          v-else-if="!isAdmin && !isRegistered && call.is_active"
          type="button"
          @click="handleEnrollment"
          :disabled="submitting"
          class="app-btn-accent tw-inline-flex tw-items-center tw-justify-center tw-px-8 tw-gap-2 tw-text-sm"
        >
          <span class="material-symbols-outlined tw-text-[18px]">how_to_reg</span>
          Inscribirme ahora
        </button>
      </div>
    </div>

    <!-- BANNER ESTADO -->
    <div v-if="!isAdmin && isRegistered" class="tw-flex tw-items-center tw-gap-4 tw-p-4 tw-rounded-xl tw-bg-[rgba(47,143,91,0.1)] tw-border tw-border-[var(--app-success)]">
      <span class="material-symbols-outlined tw-text-[var(--app-success)]">check_circle</span>
      <div>
        <p class="tw-text-sm tw-font-bold tw-text-[var(--app-ink-900)]">Ya estás inscrito</p>
        <p class="tw-text-xs tw-text-[var(--app-slate-600)]">Accede a "Mi Proyecto" para gestionar tus avances.</p>
      </div>
    </div>

    <!-- SECCIÓN GENERAL -->
    <div class="app-card-glass tw-p-8">
      <div class="tw-space-y-6">
        <div>
          <label class="tw-text-[10px] tw-uppercase tw-tracking-widest tw-font-bold tw-text-[var(--app-slate-400)]">Título</label>
          <input v-if="isEditing" v-model="editForm.title" class="tw-w-full tw-mt-2 tw-p-3 tw-bg-[var(--app-surface-container-lowest)] tw-rounded-lg tw-border tw-border-[var(--app-outline-variant)] focus:tw-border-[var(--app-primary)] focus:tw-ring-2 focus:tw-ring-[var(--app-input-focus-ring)] tw-transition-all tw-outline-none" />
          <h3 v-else class="tw-text-xl tw-font-medium tw-text-[var(--app-ink-800)] tw-mt-1">{{ call.title }}</h3>
        </div>

        <div>
          <label class="tw-text-[10px] tw-uppercase tw-tracking-widest tw-font-bold tw-text-[var(--app-slate-400)]">Descripción</label>
          <textarea v-if="isEditing" v-model="editForm.description" rows="4" class="tw-w-full tw-mt-2 tw-p-3 tw-bg-[var(--app-surface-container-lowest)] tw-rounded-lg tw-border tw-border-[var(--app-outline-variant)] focus:tw-border-[var(--app-primary)] focus:tw-ring-2 focus:tw-ring-[var(--app-input-focus-ring)] tw-transition-all tw-outline-none"></textarea>
          <p v-else class="tw-text-sm tw-leading-relaxed tw-text-[var(--app-slate-600)] tw-mt-1">{{ call.description }}</p>
        </div>
      </div>
    </div>

    <!-- VIGENCIA: Uso de grid para equilibrio -->
    <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-6">
      <div class="app-card-glass tw-p-6">
        <div class="tw-flex tw-items-center tw-gap-3 tw-mb-4">
          <span class="material-symbols-outlined tw-text-[var(--app-accent-brass)]">event</span>
          <span class="tw-text-xs tw-font-bold tw-uppercase tw-text-[var(--app-slate-500)]">Inicio</span>
        </div>
        <p class="tw-font-mono tw-text-lg tw-text-[var(--app-ink-900)]">{{ formatDate(call.start_date) }}</p>
      </div>

      <div class="app-card-glass tw-p-6">
        <div class="tw-flex tw-items-center tw-gap-3 tw-mb-4">
          <span class="material-symbols-outlined tw-text-[var(--app-error)]">event_busy</span>
          <span class="tw-text-xs tw-font-bold tw-uppercase tw-text-[var(--app-slate-500)]">Cierre</span>
        </div>
        <p class="tw-font-mono tw-text-lg tw-text-[var(--app-ink-900)]">{{ formatDate(call.end_date) }}</p>
      </div>
    </div>

    <!-- REQUISITOS -->
    <div class="app-card-glass tw-p-8">
      <h3 class="tw-font-bold tw-text-[var(--app-ink-900)] tw-mb-6">Requisitos de participación</h3>
      <ul class="tw-space-y-4">
        <li v-for="req in requirements" :key="req.id" class="tw-flex tw-items-start tw-gap-4 tw-p-4 tw-rounded-lg tw-bg-[var(--app-slate-50)]">
          <span class="material-symbols-outlined" :class="req.is_required ? 'tw-text-[var(--app-accent-brass)]' : 'tw-text-[var(--app-slate-300)]'">
            {{ req.is_required ? 'check_circle' : 'radio_button_unchecked' }}
          </span>
          <div>
            <p class="tw-text-sm tw-font-bold tw-text-[var(--app-ink-800)]">{{ req.title }}</p>
            <p class="tw-text-xs tw-text-[var(--app-slate-500)]">{{ req.description }}</p>
          </div>
        </li>
      </ul>
    </div>
  </section>
</template>

<script setup lang="ts">
// (Misma lógica funcional, solo importando los componentes de UI que ya tienes)
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { callService, type Call } from '../services/callService'
import type { CallWorkspace, CallRequirement } from '../services/workspaceService'
import { useWorkspaceStore } from '../stores/workspaceStore'
import { useAuthStore } from '@/stores/authStore'
import AppButton from '@/shared/components/AppButton.vue'

const props = defineProps<{
  call: Call
  workspace: CallWorkspace
}>()

const router = useRouter()
const workspaceStore = useWorkspaceStore()
const authStore = useAuthStore()

const submitting = ref(false)
const saving = ref(false)
const isEditing = ref(false)
const showAddReqModal = ref(false)

const isAdmin = computed(() => authStore.user?.role === 'admin')
const isRegistered = computed(() => props.workspace?.participant_status && props.workspace.participant_status !== 'NOT_REGISTERED')
const requirements = computed<CallRequirement[]>(() => props.workspace?.requirements ?? [])

// Formulario de edición de Convocatoria
const editForm = ref({
  title: props.call?.title || '',
  description: props.call?.description || '',
  is_active: props.call?.is_active ?? true,
  start_date: props.call?.start_date ? props.call.start_date.split('T')[0] : '',
  end_date: props.call?.end_date ? props.call.end_date.split('T')[0] : ''
})

watch(() => props.call, (newCall) => {
  if (newCall) {
    editForm.value = {
      title: newCall.title || '',
      description: newCall.description || '',
      is_active: newCall.is_active ?? true,
      start_date: newCall.start_date ? newCall.start_date.split('T')[0] : '',
      end_date: newCall.end_date ? newCall.end_date.split('T')[0] : ''
    }
  }
}, { immediate: true })

// Formulario para nuevo requisito
const newReq = ref({ title: '', description: '', is_required: true })

function cancelEdit() {
  isEditing.value = false
}

async function saveChanges() {
  try {
    saving.value = true
    await callService.updateCall(props.call.id, editForm.value)
    await workspaceStore.fetchWorkspace(props.call.id, true)
    isEditing.value = false
  } catch (error) {
    console.error('Error al actualizar la convocatoria:', error)
  } finally {
    saving.value = false
  }
}

async function handleAddRequirement() {
  if (!newReq.value.title) return
  try {
    await callService.addRequirement(props.call.id, newReq.value)
    await workspaceStore.fetchWorkspace(props.call.id, true)
    newReq.value = { title: '', description: '', is_required: true }
    showAddReqModal.value = false
  } catch (error) {
    console.error('Error al agregar requisito:', error)
  }
}

async function handleEnrollment() {
  try {
    submitting.value = true
    await callService.joinCall(props.call.id)
    await workspaceStore.fetchWorkspace(props.call.id, true)
    router.push({ name: 'call-project', params: { id: props.call.id } })
  } catch (error) {
    console.error('Error durante la inscripción:', error)
  } finally {
    submitting.value = false
  }
}

function formatDate(date?: string) {
  if (!date) return 'No disponible'
  return new Date(date).toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
}
</script>