<template>
  <section class="tw-space-y-6">
    <div>
      <div class="tw-mb-1 tw-flex tw-items-center tw-gap-2">
        <span class="material-symbols-outlined notranslate tw-text-primary">folder_special</span>
        <h2 class="tw-text-xl tw-font-bold tw-text-on-surface">Proyecto Postulado</h2>
      </div>
      <p class="tw-text-sm tw-text-on-surface-variant">
        Gestiona el proyecto con el que participas en <span class="tw-font-semibold tw-text-on-surface">{{ call.title
          }}</span>.
      </p>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="loading" class="tw-flex tw-justify-center tw-py-8">
      <span class="material-symbols-outlined notranslate tw-animate-spin tw-text-primary">progress_activity</span>
    </div>

    <!-- Vista A: Proyecto Actualmente Vinculado -->
    <div v-else-if="project" class="tw-space-y-4">
      <AppCard padding="md" variant="glass">
        <div class="tw-flex tw-items-start tw-justify-between tw-gap-4">
          <div class="tw-space-y-2 tw-w-full">
                <!-- Botón de Envío de Postulación -->
          <AppCard v-if="project.status === 'draft'" padding="md" variant="flat"
            class="tw-bg-surface-container-low tw-border tw-border-primary/20">
            <div class="tw-flex tw-items-center tw-justify-between">
              <div>
                <h4 class="tw-text-sm tw-font-semibold tw-text-on-surface">¿Todo listo con tu propuesta?</h4>
                <p class="tw-text-xs tw-text-on-surface-variant">
                  Una vez que envíes tu proyecto, pasará a revisión y ya no podrás modificar los documentos.
                </p>
              </div>
              <button type="button" @click="handleSubmitProposal" :disabled="saving"
                class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-sm tw-font-medium hover:tw-bg-primary/90 tw-transition-colors disabled:tw-opacity-50 tw-flex tw-items-center tw-gap-2">
                <span class="material-symbols-outlined notranslate tw-text-sm">send</span>
                {{ saving ? 'Enviando...' : 'Enviar Propuesta' }}
              </button>
            </div>
          </AppCard>
            <div class="tw-flex tw-items-center tw-justify-between tw-w-full">
              <div class="tw-flex tw-items-center tw-gap-2">
                <h3 class="tw-text-lg tw-font-bold tw-text-on-surface">{{ project.title }}</h3>
                <AppBadge :variant="getStatusVariant(project.status)">
                  {{ project.status || 'draft' }}
                </AppBadge>
              </div>
              
              <button type="button" @click="isEditing = !isEditing"
                class="tw-flex tw-items-center tw-gap-1 tw-px-3 tw-py-1.5 tw-text-xs tw-font-medium tw-rounded-lg tw-bg-surface-container hover:tw-bg-surface-container-high tw-text-on-surface tw-transition-colors">
                <span class="material-symbols-outlined notranslate tw-text-sm">
                  {{ isEditing ? 'close' : 'edit' }}
                </span>
                {{ isEditing ? 'Cancelar' : 'Editar' }}
              </button>
            </div>

            <p class="tw-text-sm tw-text-on-surface-variant">
              {{ project.description || 'Sin descripción provista.' }}
            </p>

            <!-- Retroalimentación del Evaluador (Si existe) -->
<div v-if="project.feedback" class="tw-mt-4 tw-p-4 tw-rounded-xl tw-bg-surface-container-low tw-border tw-border-outline-variant tw-space-y-1">
  <div class="tw-flex tw-items-center tw-gap-2">
    <span class="material-symbols-outlined notranslate tw-text-primary tw-text-sm">rate_review</span>
    <h4 class="tw-text-xs tw-font-semibold tw-text-primary tw-uppercase tw-tracking-wider">
      Retroalimentación del Evaluador
    </h4>
  </div>
  <p class="tw-text-sm tw-text-on-surface">
    {{ project.feedback }}
  </p>
</div>
          </div>
        </div>
      </AppCard>

      <!-- Formulario de Edición -->
      <AppCard v-if="isEditing" padding="md" variant="flat">
        <h4 class="tw-text-sm tw-font-semibold tw-text-on-surface tw-mb-3">Editar Detalles del Proyecto</h4>
        <form @submit.prevent="handleUpdateProject" class="tw-space-y-4">
          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Título del Proyecto *
            </label>
            <input v-model="editForm.title" type="text" required
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none" />
          </div>

          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Categoría del Proyecto
            </label>
            <input type="text" v-model="editForm.category"
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none" />
          </div>

          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Descripción del Proyecto
            </label>
            <textarea v-model="editForm.description" rows="3"
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none"></textarea>
          </div>

          <div class="tw-flex tw-justify-end tw-gap-2">
            <button type="submit" :disabled="saving"
              class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-sm tw-font-medium hover:tw-bg-primary/90 tw-transition-colors disabled:tw-opacity-50">
              {{ saving ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </AppCard>

      <!-- SECCIÓN DE DOCUMENTOS DEL PROYECTO -->
      <AppCard padding="md" variant="flat" class="tw-mt-6">
        <div class="tw-flex tw-items-center tw-justify-between tw-mb-4">
          <div>
            <h4 class="tw-text-base tw-font-semibold tw-text-on-surface">Documentos del Proyecto</h4>
            <p class="tw-text-xs tw-text-on-surface-variant">
              Adjunta los requisitos técnicos y administrativos necesarios para esta propuesta.
            </p>
          </div>
          <div>
            <input type="file" ref="fileInput" class="tw-hidden" @change="handleFileUpload" />
            <button type="button" @click="fileInput?.click()" :disabled="uploadingDoc"
              class="tw-flex tw-items-center tw-gap-1.5 tw-px-3 tw-py-1.5 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-xs tw-font-medium hover:tw-bg-primary/90 tw-transition-colors disabled:tw-opacity-50">
              <span class="material-symbols-outlined notranslate tw-text-sm">upload_file</span>
              {{ uploadingDoc ? 'Subiendo...' : 'Subir Archivo' }}
            </button>
          </div>
        </div>

        <!-- Estado Vacío -->
        <div v-if="projectDocuments.length === 0"
          class="tw-text-center tw-py-6 tw-border tw-border-dashed tw-border-outline-variant tw-rounded-lg">
          <span class="material-symbols-outlined notranslate tw-text-3xl tw-text-outline tw-mb-1">folder_off</span>
          <p class="tw-text-xs tw-text-on-surface-variant">No se han subido documentos a este proyecto.</p>
        </div>

        <!-- Lista de Archivos Cargados -->
        <div v-else class="tw-space-y-2">
          <div v-for="doc in projectDocuments" :key="doc.id"
            class="tw-flex tw-items-center tw-justify-between tw-p-3 tw-rounded-lg tw-bg-surface-container-lowest tw-border tw-border-outline-variant hover:tw-border-primary/40 tw-transition-colors">
            <div class="tw-flex tw-items-center tw-gap-3 tw-overflow-hidden">
              <span class="material-symbols-outlined notranslate tw-text-primary">description</span>
              <div class="tw-truncate">
                <p class="tw-text-sm tw-font-medium tw-text-on-surface tw-truncate">
                  {{ doc.original_filename || doc.filename }}
                </p>
                <p class="tw-text-xs tw-text-on-surface-variant">
                  {{ (doc.file_size / 1024).toFixed(1) }} KB • {{ new Date(doc.created_at).toLocaleDateString() }}
                </p>
              </div>
            </div>

            <div class="tw-flex tw-items-center tw-gap-1">
              <button type="button" @click="handleDownloadDocument(doc)"
                class="tw-p-1.5 tw-rounded-md hover:tw-bg-surface-container tw-text-on-surface-variant hover:tw-text-primary tw-transition-colors"
                title="Descargar">
                <span class="material-symbols-outlined notranslate tw-text-sm">download</span>
              </button>
              <button type="button" @click="handleDeleteDocument(doc.id)"
                class="tw-p-1.5 tw-rounded-md hover:tw-bg-surface-container tw-text-on-surface-variant hover:tw-text-error tw-transition-colors"
                title="Eliminar">
                <span class="material-symbols-outlined notranslate tw-text-sm">delete</span>
              </button>
            </div>
          </div>
        </div>
      </AppCard>
    </div>

    <!-- Vista B: Selección o Creación de Proyecto -->
    <div v-else class="tw-space-y-4">
      <!-- Selector de Modo -->
      <div class="tw-flex tw-border-b tw-border-outline-variant">
        <button type="button" @click="mode = 'select'"
          class="tw-px-4 tw-py-2 tw-text-sm tw-font-medium tw-border-b-2 tw-transition-colors"
          :class="mode === 'select' ? 'tw-border-primary tw-text-primary' : 'tw-border-transparent tw-text-on-surface-variant hover:tw-text-on-surface'">
          Vincular Proyecto Existente
        </button>
        <button type="button" @click="mode = 'create'"
          class="tw-px-4 tw-py-2 tw-text-sm tw-font-medium tw-border-b-2 tw-transition-colors"
          :class="mode === 'create' ? 'tw-border-primary tw-text-primary' : 'tw-border-transparent tw-text-on-surface-variant hover:tw-text-on-surface'">
          Crear Nuevo Proyecto
        </button>
      </div>

      <!-- Opción A: Seleccionar proyecto existente -->
      <AppCard v-if="mode === 'select'" padding="md" variant="flat">
        <h3 class="tw-text-base tw-font-semibold tw-text-on-surface tw-mb-3">
          Selecciona uno de tus proyectos
        </h3>

        <div v-if="userProjects.length === 0" class="tw-text-sm tw-text-on-surface-variant tw-py-4">
          No tienes proyectos registrados previamente. Usa la pestaña "Crear Nuevo Proyecto".
        </div>

        <form v-else @submit.prevent="handleLinkExistingProject" class="tw-space-y-4">
          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Proyecto a vincular
            </label>
            <select v-model="selectedProjectId" required
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-2.5 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none">
              <option :value="null" disabled>Selecciona un proyecto...</option>
              <option v-for="p in userProjects" :key="p.id" :value="p.id">
                {{ p.title }}
              </option>
            </select>
          </div>

          <button type="submit" :disabled="!selectedProjectId || saving"
            class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-sm tw-font-medium hover:tw-bg-primary/90 tw-transition-colors disabled:tw-opacity-50">
            {{ saving ? 'Vincular...' : 'Vincular Selección' }}
          </button>
        </form>
      </AppCard>

      <!-- Opción B: Crear nuevo proyecto -->
      <AppCard v-else padding="md" variant="flat">
        <h3 class="tw-text-base tw-font-semibold tw-text-on-surface tw-mb-4">
          Registrar y vincular un nuevo proyecto
        </h3>
        <form @submit.prevent="handleCreateProject" class="tw-space-y-4">
          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Título del Proyecto *
            </label>
            <input v-model="createForm.title" type="text" required placeholder="Ej. Sistema de Monitoreo Agrícola"
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-3 tw-py-2 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none" />
          </div>

          <div>
            <label class="tw-block tw-text-xs tw-font-medium tw-text-on-surface-variant tw-mb-1">
              Descripción del Proyecto
            </label>
            <textarea v-model="createForm.description" rows="3"
              class="tw-w-full tw-rounded-lg tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-p-3 tw-text-sm tw-text-on-surface focus:tw-border-accent focus:tw-outline-none"
              placeholder="Detalla los objetivos, problemática y propuesta..."></textarea>
          </div>

          <button type="submit" :disabled="saving"
            class="tw-px-4 tw-py-2 tw-rounded-lg tw-bg-primary tw-text-on-primary tw-text-sm tw-font-medium hover:tw-bg-primary/90 tw-transition-colors disabled:tw-opacity-50">
            {{ saving ? 'Creando...' : 'Crear y Vincular Proyecto' }}
          </button>
        </form>
      </AppCard>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { projectService, type Project } from '@/modules/projects/services/projectService'
import type { Call } from '../services/callService'
import type { CallWorkspace } from '../services/workspaceService'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'

const props = defineProps<{
  call: Call
  workspace: CallWorkspace | null
}>()

const project = ref<Project | null>(null)
const userProjects = ref<Project[]>([])
const projectDocuments = ref<DocumentModel[]>([])

const loading = ref(true)
const saving = ref(false)
const uploadingDoc = ref(false)
const isEditing = ref(false)
const mode = ref<'select' | 'create'>('create')
const selectedProjectId = ref<number | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)

const createForm = ref({
  title: '',
  description: '',
  category: '',
  status: 'draft'
})

const editForm = ref({
  title: '',
  description: '',
  category: '',
  status: 'draft'
})

async function fetchProjectDocuments(projectId: number) {
  try {
    const docs = await documentService.getDocuments({ project_id: projectId })
    projectDocuments.value = docs
  } catch (err) {
    console.error('Error al cargar documentos del proyecto:', err)
  }
}

async function fetchCallProject() {
  try {
    loading.value = true
    const allUserProjects = await projectService.getAll()
    userProjects.value = allUserProjects

    const callProjects = await projectService.getAll({ call_id: props.call.id })
    if (callProjects.length > 0) {
      const activeProject = callProjects[0] ?? null
      project.value = activeProject
      if (activeProject) {
        populateEditForm(activeProject)
        await fetchProjectDocuments(activeProject.id)
      }
    }
  } catch (err) {
    console.error('Error al cargar proyectos:', err)
  } finally {
    loading.value = false
  }
}

function populateEditForm(proj: Project) {
  editForm.value = {
    title: proj.title || '',
    description: proj.description || '',
    category: proj.category || '',
    status: proj.status || 'draft'
  }
}

async function handleSubmitProposal() {
  if (!project.value) return
  if (!confirm('¿Estás seguro de enviar tu propuesta? Una vez enviada, cambiará de estado.')) return

  try {
    saving.value = true
    const updated = await projectService.update(project.value.id, {
      status: 'submitted'
    })
    project.value = updated
    populateEditForm(updated)
  } catch (err) {
    console.error('Error al enviar la propuesta:', err)
  } finally {
    saving.value = false
  }
}

async function handleLinkExistingProject() {
  if (!selectedProjectId.value) return
  try {
    saving.value = true
    const updated = await projectService.update(selectedProjectId.value, {
      call_id: props.call.id
    })
    project.value = updated
    populateEditForm(updated)
    await fetchProjectDocuments(updated.id)
  } catch (err) {
    console.error('Error al vincular el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleCreateProject() {
  if (!createForm.value.title.trim()) return
  try {
    saving.value = true
    const newProject = await projectService.create({
      title: createForm.value.title,
      description: createForm.value.description,
      call_id: props.call.id,
      status: createForm.value.status
    })
    project.value = newProject
    populateEditForm(newProject)
    await fetchProjectDocuments(newProject.id)
  } catch (err) {
    console.error('Error al crear el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleUpdateProject() {
  if (!project.value) return
  try {
    saving.value = true
    const updated = await projectService.update(project.value.id, {
      title: editForm.value.title,
      description: editForm.value.description,
      status: editForm.value.status
    })
    project.value = updated
    isEditing.value = false
  } catch (err) {
    console.error('Error al actualizar el proyecto:', err)
  } finally {
    saving.value = false
  }
}

async function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file || !project.value) return

  const formData = new FormData()
  formData.append('file', file) // 'file' ahora es puramente de tipo 'File' (Blob)
  formData.append('project_id', project.value.id.toString())
  formData.append('call_id', props.call.id.toString())

  try {
    uploadingDoc.value = true
    await documentService.uploadDocument(formData)
    await fetchProjectDocuments(project.value.id)
  } catch (err) {
    console.error('Error al subir documento:', err)
  } finally {
    uploadingDoc.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}
async function handleDownloadDocument(doc: DocumentModel) {
  try {
    await documentService.downloadDocument(doc.id, doc.original_filename || doc.filename)
  } catch (err) {
    console.error('Error al descargar archivo:', err)
  }
}

async function handleDeleteDocument(docId: number) {
  if (!confirm('¿Deseas eliminar este documento del proyecto?')) return
  try {
    await documentService.deleteDocument(docId)
    if (project.value) {
      await fetchProjectDocuments(project.value.id)
    }
  } catch (err) {
    console.error('Error al eliminar archivo:', err)
  }
}

function getStatusVariant(status?: string) {
  switch (status) {
    case 'approved': return 'success'
    case 'rejected': return 'error'
    case 'submitted': return 'warning'
    default: return 'secondary'
  }
}

onMounted(() => {
  fetchCallProject()
})
</script>