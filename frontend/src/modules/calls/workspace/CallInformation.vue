<template>
  <section class="tw-space-y-6">
    <!-- ENCABEZADO Y ACCIONES PRINCIPALES -->
    <div class="tw-flex tw-items-center tw-justify-between tw-flex-wrap tw-gap-4">
      <div>
        <div class="tw-flex tw-items-center tw-gap-2 tw-mb-1">
          <span class="material-symbols-outlined notranslate tw-text-primary">info</span>
          <h2 class="tw-text-xl tw-font-bold tw-text-on-surface">Información de la convocatoria</h2>
        </div>
        <p class="tw-text-sm tw-text-on-surface-variant">
          {{ isAdmin ? 'Administra los detalles y requisitos de esta convocatoria.' : 'Consulta los detalles, fechas y condiciones de esta convocatoria.' }}
        </p>
      </div>

      <!-- BOTONES DE ACCIÓN (ADMIN VS ESTUDIANTE) -->
      <div>
        <!-- Modo lectura Admin: Botón Editar -->
        <AppButton 
          v-if="isAdmin && !isEditing" 
          variant="primary" 
          icon="edit" 
          @click="isEditing = true"
        >
          Editar Convocatoria
        </AppButton>

        <!-- Modo edición Admin: Cancelar / Guardar -->
        <div v-else-if="isAdmin && isEditing" class="tw-flex tw-gap-2">
          <AppButton variant="secondary" icon="cancel" @click="cancelEdit">
            Cancelar
          </AppButton>
          <AppButton variant="primary" icon="save" :loading="saving" @click="saveChanges">
            Guardar Cambios
          </AppButton>
        </div>

        <!-- CTA Inscribirse: Solo Estudiante no registrado -->
        <button
          v-else-if="!isAdmin && !isRegistered && call.is_active"
          type="button"
          @click="handleEnrollment"
          :disabled="submitting"
          class="tw-inline-flex tw-items-center tw-gap-2 tw-rounded-xl tw-bg-primary tw-px-5 tw-py-2.5 tw-text-sm tw-font-semibold tw-text-on-primary tw-shadow-md tw-transition hover:tw-bg-primary-hover focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-primary/40 disabled:tw-opacity-50"
        >
          <span v-if="submitting" class="material-symbols-outlined notranslate tw-animate-spin">progress_activity</span>
          <span v-else class="material-symbols-outlined notranslate">how_to_reg</span>
          <span>Inscribirme a la convocatoria</span>
        </button>
      </div>
    </div>

    <!-- BANNER DE INSCRITO (Solo Estudiantes) -->
    <AppCard
      v-if="!isAdmin && isRegistered"
      variant="glass"
      padding="md"
      class="tw-border-l-4 tw-border-l-success"
    >
      <div class="tw-flex tw-items-center tw-gap-3">
        <span class="material-symbols-outlined notranslate tw-text-success">check_circle</span>
        <div>
          <p class="tw-text-sm tw-font-semibold tw-text-on-surface">Ya estás inscrito en esta convocatoria</p>
          <p class="tw-text-xs tw-text-on-surface-variant">
            Puedes acceder a la pestaña <strong>"Mi Proyecto"</strong> para comenzar a cargar tus avances.
          </p>
        </div>
      </div>
    </AppCard>

    <!-- INFORMACIÓN GENERAL (MODO LECTURA / EDICIÓN) -->
    <AppCard variant="glass" padding="md">
      <div class="tw-flex tw-items-center tw-gap-2 tw-mb-5">
        <span class="material-symbols-outlined notranslate tw-text-primary">campaign</span>
        <h3 class="tw-font-semibold tw-text-on-surface">Información general</h3>
      </div>

      <div class="tw-space-y-5">
        <!-- TÍTULO -->
        <div>
          <label class="tw-block tw-text-xs tw-font-medium tw-text-outline tw-mb-1">
            Nombre de la convocatoria
          </label>
          <input 
            v-if="isEditing" 
            v-model="editForm.title" 
            type="text" 
            class="tw-w-full tw-px-3 tw-py-2 tw-rounded-xl tw-bg-surface-container-low tw-border tw-border-outline-variant tw-text-sm tw-text-on-surface focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-primary"
          />
          <p v-else class="tw-text-base tw-font-semibold tw-text-on-surface">
            {{ call.title || 'Sin título' }}
          </p>
        </div>

        <!-- DESCRIPCIÓN -->
        <div>
          <label class="tw-block tw-text-xs tw-font-medium tw-text-outline tw-mb-1">
            Descripción
          </label>
          <textarea 
            v-if="isEditing" 
            v-model="editForm.description" 
            rows="3"
            class="tw-w-full tw-px-3 tw-py-2 tw-rounded-xl tw-bg-surface-container-low tw-border tw-border-outline-variant tw-text-sm tw-text-on-surface focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-primary"
          ></textarea>
          <p v-else class="tw-text-sm tw-leading-relaxed tw-text-on-surface-variant">
            {{ call.description || 'Esta convocatoria no cuenta con una descripción disponible.' }}
          </p>
        </div>

        <!-- ESTADO -->
        <div>
          <label class="tw-block tw-text-xs tw-font-medium tw-text-outline tw-mb-2">
            Estado
          </label>
          <div v-if="isEditing" class="tw-flex tw-items-center tw-gap-3">
            <label class="tw-flex tw-items-center tw-gap-2 tw-text-sm tw-cursor-pointer">
              <input type="checkbox" v-model="editForm.is_active" class="tw-rounded tw-text-primary" />
              <span>Convocatoria Activa / Abierta</span>
            </label>
          </div>
          <AppBadge v-else :variant="call.is_active ? 'success' : 'neutral'" :dot="true">
            {{ call.is_active ? 'Convocatoria abierta' : 'Convocatoria cerrada' }}
          </AppBadge>
        </div>
      </div>
    </AppCard>

    <!-- VIGENCIA (FECHAS) -->
    <AppCard variant="glass" padding="md">
      <div class="tw-flex tw-items-center tw-gap-2 tw-mb-5">
        <span class="material-symbols-outlined notranslate tw-text-primary">calendar_month</span>
        <div>
          <h3 class="tw-font-semibold tw-text-on-surface">Vigencia</h3>
          <p class="tw-text-xs tw-text-on-surface-variant">Periodo disponible para participar en la convocatoria.</p>
        </div>
      </div>

      <div class="tw-grid tw-grid-cols-1 md:tw-grid-cols-2 tw-gap-4">
        <!-- Inicio -->
        <div class="tw-rounded-xl tw-bg-surface-container-low tw-p-4">
          <div class="tw-flex tw-items-center tw-gap-2 tw-mb-3">
            <span class="material-symbols-outlined notranslate tw-text-success">event</span>
            <span class="tw-text-xs tw-font-medium tw-text-outline">Fecha de inicio</span>
          </div>
          <input 
            v-if="isEditing" 
            v-model="editForm.start_date" 
            type="date" 
            class="tw-w-full tw-px-3 tw-py-1.5 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
          />
          <p v-else class="tw-text-base tw-font-semibold tw-text-on-surface">
            {{ formatDate(call.start_date) }}
          </p>
        </div>

        <!-- Cierre -->
        <div class="tw-rounded-xl tw-bg-surface-container-low tw-p-4">
          <div class="tw-flex tw-items-center tw-gap-2 tw-mb-3">
            <span class="material-symbols-outlined notranslate tw-text-warning">event_busy</span>
            <span class="tw-text-xs tw-font-medium tw-text-outline">Fecha de cierre</span>
          </div>
          <input 
            v-if="isEditing" 
            v-model="editForm.end_date" 
            type="date" 
            class="tw-w-full tw-px-3 tw-py-1.5 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
          />
          <p v-else class="tw-text-base tw-font-semibold tw-text-on-surface">
            {{ formatDate(call.end_date) }}
          </p>
        </div>
      </div>
    </AppCard>

    <!-- REQUISITOS (LECTURA Y CREACIÓN RÁPIDA PARA ADMIN) -->
    <AppCard variant="glass" padding="md">
      <div class="tw-mb-5 tw-flex tw-items-center tw-justify-between tw-gap-4">
        <div class="tw-flex tw-items-center tw-gap-2">
          <span class="material-symbols-outlined notranslate tw-text-primary">checklist</span>
          <div>
            <h3 class="tw-font-semibold tw-text-on-surface">Requisitos de participación</h3>
            <p class="tw-text-xs tw-text-on-surface-variant">Condiciones para participar en esta convocatoria</p>
          </div>
        </div>

        <!-- Admin: Agregar Requisito Rápido -->
        <AppButton 
          v-if="isAdmin" 
          variant="outline" 
          size="sm" 
          icon="add" 
          @click="showAddReqModal = !showAddReqModal"
        >
          {{ showAddReqModal ? 'Cancelar' : 'Añadir Requisito' }}
        </AppButton>
      </div>

      <!-- Formulario para agregar nuevo requisito (Admin) -->
      <div v-if="isAdmin && showAddReqModal" class="tw-mb-5 tw-p-4 tw-rounded-xl tw-bg-surface-container-low tw-space-y-3 tw-border tw-border-outline-variant/40">
        <input 
          v-model="newReq.title" 
          placeholder="Nombre del requisito (ej. Anteproyecto en PDF)"
          class="tw-w-full tw-px-3 tw-py-2 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
        />
        <textarea 
          v-model="newReq.description" 
          placeholder="Instrucciones o especificaciones opcionales"
          class="tw-w-full tw-px-3 tw-py-2 tw-rounded-lg tw-bg-surface tw-border tw-border-outline-variant tw-text-sm"
          rows="2"
        ></textarea>
        <div class="tw-flex tw-items-center tw-justify-between">
          <label class="tw-flex tw-items-center tw-gap-2 tw-text-xs tw-text-on-surface-variant">
            <input type="checkbox" v-model="newReq.is_required" /> Obligatorio
          </label>
          <AppButton size="sm" variant="primary" :disabled="!newReq.title" @click="handleAddRequirement">
            Guardar Requisito
          </AppButton>
        </div>
      </div>

      <!-- Lista de Requisitos -->
      <div v-if="requirements.length > 0" class="tw-space-y-3">
        <div
          v-for="requirement in requirements"
          :key="requirement.id"
          class="tw-flex tw-items-start tw-gap-3 tw-rounded-xl tw-border tw-border-outline-variant/60 tw-bg-surface-container-lowest tw-p-4"
        >
          <span
            class="material-symbols-outlined notranslate tw-mt-0.5 tw-text-xl"
            :class="[requirement.is_required ? 'tw-text-accent' : 'tw-text-on-surface-variant']"
          >
            {{ requirement.is_required ? 'check_circle' : 'radio_button_unchecked' }}
          </span>

          <div class="tw-min-w-0 tw-flex-1">
            <p
              class="tw-text-sm tw-font-semibold"
              :class="requirement.is_required ? 'tw-text-on-surface' : 'tw-text-on-surface-variant'"
            >
              {{ requirement.title }}
            </p>

            <p v-if="requirement.description" class="tw-mt-1 tw-text-sm tw-leading-relaxed tw-text-on-surface-variant">
              {{ requirement.description }}
            </p>
          </div>

          <span
            v-if="requirement.is_required"
            class="tw-shrink-0 tw-rounded-md tw-bg-accent-bg tw-px-2 tw-py-1 tw-text-[11px] tw-font-medium tw-text-accent"
          >
            Obligatorio
          </span>
        </div>
      </div>

      <div v-else class="tw-rounded-xl tw-border tw-border-dashed tw-border-outline-variant tw-bg-surface-container-low tw-p-8">
        <div class="tw-flex tw-flex-col tw-items-center tw-text-center">
          <h4 class="tw-font-semibold tw-text-on-surface">Requisitos por publicar</h4>
          <p class="tw-mt-1 tw-max-w-md tw-text-sm tw-text-on-surface-variant">
            Esta convocatoria todavía no ha publicado los requisitos de participación.
          </p>
        </div>
      </div>
    </AppCard>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import type { Call } from '../services/callService'
import { callService } from '../services/callService'
import type { CallWorkspace, CallRequirement } from '../services/workspaceService'
import { useWorkspaceStore } from '../stores/workspaceStore'
import { useAuthStore } from '@/stores/authStore'
import AppButton from '@/shared/components/AppButton.vue'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'

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