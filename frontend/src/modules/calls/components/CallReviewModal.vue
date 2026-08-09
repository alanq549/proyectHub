<!-- src/modules/calls/components/CallReviewModal.vue -->
<template>
  <div class="tw-fixed tw-inset-0 tw-z-50 tw-flex tw-items-center tw-justify-center tw-bg-black/50 tw-p-4">
    <AppCard variant="glass" padding="lg" class="tw-w-full tw-max-w-2xl tw-max-h-[90vh] tw-overflow-y-auto tw-space-y-6">
      <div class="tw-flex tw-items-center tw-justify-between tw-border-b tw-border-outline-variant tw-pb-4">
        <div>
          <h3 class="tw-text-lg tw-font-bold tw-text-on-surface">Revisión de Propuesta</h3>
          <p class="tw-text-xs tw-text-on-surface-variant">{{ project.title }}</p>
        </div>
        <button @click="$emit('close')" class="tw-text-on-surface-variant hover:tw-text-on-surface">
          <span class="material-symbols-outlined notranslate">close</span>
        </button>
      </div>

      <!-- Detalles del Proyecto -->
      <div class="tw-space-y-2">
        <h4 class="tw-text-sm tw-font-semibold tw-text-on-surface">Descripción</h4>
        <p class="tw-text-sm tw-text-on-surface-variant tw-bg-surface-container-lowest tw-p-3 tw-rounded-lg tw-border tw-border-outline-variant">
          {{ project.description || 'Sin descripción provista.' }}
        </p>
      </div>

      <!-- Documentos Adjuntos del Alumno -->
      <div class="tw-space-y-2">
        <h4 class="tw-text-sm tw-font-semibold tw-text-on-surface">Archivos Entregables</h4>
        <div v-if="documents.length === 0" class="tw-text-xs tw-text-on-surface-variant tw-italic">
          El alumno aún no ha subido archivos a este proyecto.
        </div>
        <div v-else class="tw-space-y-2">
          <div v-for="doc in documents" :key="doc.id" class="tw-flex tw-items-center tw-justify-between tw-p-2.5 tw-rounded-lg tw-bg-surface-container-lowest tw-border tw-border-outline-variant">
            <div class="tw-flex tw-items-center tw-gap-2 tw-truncate">
              <span class="material-symbols-outlined notranslate tw-text-primary tw-text-sm">description</span>
              <span class="tw-text-xs tw-font-medium tw-text-on-surface tw-truncate">{{ doc.original_filename || doc.filename }}</span>
            </div>
            <button @click="handleDownload(doc)" type="button" class="tw-p-1 tw-rounded hover:tw-bg-surface-container tw-text-primary" title="Descargar">
              <span class="material-symbols-outlined notranslate tw-text-sm">download</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Formulario de Evaluación / Estado y Comentarios -->
      <form @submit.prevent="handleSubmitReview" class="tw-space-y-4 tw-border-t tw-border-outline-variant tw-pt-4">
        <div>
          <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
            Estado de la Propuesta
          </label>
          <select v-model="form.status" class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-2.5 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none">
            <option value="draft">Borrador / Pendiente</option>
            <option value="submitted">Enviado / En Revisión</option>
            <option value="approved">Aprobado</option>
            <option value="rejected">Rechazado</option>
          </select>
        </div>

        <div>
          <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
            Comentarios / Retroalimentación para el Alumno
          </label>
          <textarea v-model="form.feedback" rows="3" placeholder="Escribe observaciones o puntos de mejora..." class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none"></textarea>
        </div>

        <div class="tw-flex tw-justify-end tw-gap-2">
          <button type="button" @click="$emit('close')" class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-surface-container tw-text-on-surface tw-text-sm tw-font-medium">
            Cancelar
          </button>
          <button type="submit" :disabled="saving" class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-sm tw-font-medium hover:tw-bg-primary/90 disabled:tw-opacity-50">
            {{ saving ? 'Guardando...' : 'Guardar Evaluación' }}
          </button>
        </div>
      </form>
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { projectService, type Project } from '@/modules/projects/services/projectService'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'
import AppCard from '@/shared/components/AppCard.vue'

const props = defineProps<{
  project: Project
}>()

const emit = defineEmits(['close', 'updated'])

const documents = ref<DocumentModel[]>([])
const saving = ref(false)
const form = ref({
  status: props.project.status || 'submitted',
  feedback: props.project.feedback || ''
})

async function loadDocuments() {
  try {
    documents.value = await documentService.getDocuments({ project_id: props.project.id })
  } catch (err) {
    console.error('Error al cargar documentos del proyecto:', err)
  }
}

async function handleDownload(doc: DocumentModel) {
  try {
    await documentService.downloadDocument(doc.id, doc.original_filename || doc.filename)
  } catch (err) {
    console.error('Error al descargar:', err)
  }
}

async function handleSubmitReview() {
  try {
    saving.value = true
    // Aquí actualizas el proyecto con el nuevo estado y feedback (asegúrate de que tu projectService soporte 'feedback' o el campo correspondiente)
    await projectService.update(props.project.id, {
      status: form.value.status,
      feedback: form.value.feedback
    })
    emit('updated')
    emit('close')
  } catch (err) {
    console.error('Error al actualizar la revisión:', err)
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadDocuments()
})
</script>