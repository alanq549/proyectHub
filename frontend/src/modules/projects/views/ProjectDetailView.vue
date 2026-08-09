<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { projectService, type Project } from '../services/projectService'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'

const route = useRoute()
const router = useRouter()

const project = ref<Project | null>(null)
const documents = ref<DocumentModel[]>([])
const loading = ref(true)
const loadingDocs = ref(false)
const error = ref<string | null>(null)
const docError = ref<string | null>(null)

const loadProjectData = async () => {
  const id = route.params.id as string
  loading.value = true
  error.value = null
  try {
    // 1. Cargamos el proyecto
    project.value = await projectService.getById(id)
    
    // 2. Una vez obtenido el id del proyecto, consultamos sus documentos asociados
    if (project.value?.id) {
      loadingDocs.value = true
      docError.value = null
      try {
        documents.value = await documentService.getDocuments({ project_id: project.value.id })
      } catch (err: any) {
        docError.value = err?.response?.data?.message || 'Error al cargar los documentos.'
      } finally {
        loadingDocs.value = false
      }
    }
  } catch (err: any) {
    error.value = err?.response?.data?.message || 'Error al obtener el proyecto.'
  } finally {
    loading.value = false
  }
}

const handleDownload = async (doc: DocumentModel) => {
  try {
    await documentService.downloadDocument(doc.id, doc.original_filename || doc.filename)
  } catch (err: any) {
    alert('Error al descargar el documento')
  }
}

const goBack = () => {
  router.push({ name: 'projects-list' })
}

onMounted(() => {
  loadProjectData()
})
</script>

<template>
  <div class="project-detail-container">
    <button class="btn-back" @click="goBack">&larr; Volver a lista</button>

    <div v-if="loading" class="state-message">Cargando detalle del proyecto...</div>

    <div v-else-if="error" class="state-message error">{{ error }}</div>

    <!-- VISTA DUAL: Contenedor principal en Grid de 2 columnas -->
    <div v-else-if="project" class="dual-view-layout">
      
      <!-- COLUMNA IZQUIERDA: Detalle actual del proyecto -->
      <div class="detail-card">
        <div>
          <header class="detail-header">
            <h1>{{ project.title }}</h1>
            <div class="meta">
              <span v-if="project.category" class="badge">{{ project.category }}</span>
              <span v-if="project.status" class="status">{{ project.status }}</span>
            </div>
          </header>

          <section class="detail-body">
            <h3>Descripción</h3>
            <p>{{ project.description }}</p>

            <!-- Retroalimentación del Evaluador (Si existe) -->
            <div v-if="project.feedback" class="feedback-section">
              <h3>Retroalimentación del Evaluador</h3>
              <p class="feedback-text">{{ project.feedback }}</p>
            </div>
          </section>
        </div>

        <footer class="detail-footer">
          <small v-if="project.created_at">Creado: {{ new Date(project.created_at).toLocaleDateString() }}</small>
        </footer>
      </div>

      <!-- COLUMNA DERECHA: Apartado de documentos -->
      <div class="documents-card">
        <header class="documents-header">
          <h3>Documentos del Proyecto</h3>
        </header>

        <div class="documents-body">
          <div v-if="loadingDocs" class="state-message-sm">Cargando documentos...</div>
          
          <div v-else-if="docError" class="state-message-sm error">{{ docError }}</div>

          <div v-else-if="documents.length === 0" class="state-message-sm">
            No hay documentos asociados a este proyecto.
          </div>

          <ul v-else class="document-list">
            <li v-for="doc in documents" :key="doc.id" class="document-item">
              <div class="doc-info">
                <span class="doc-name" :title="doc.original_filename">{{ doc.original_filename || doc.filename }}</span>
                <span class="doc-date">{{ new Date(doc.created_at).toLocaleDateString() }}</span>
              </div>
              <div class="doc-actions">
                <button class="btn-action download" @click="handleDownload(doc)" title="Descargar">
                  Descargar
                </button>
              </div>
            </li>
          </ul>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
.project-detail-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.btn-back {
  background: none;
  border: none;
  color: #42b883;
  font-size: 1rem;
  cursor: pointer;
  margin-bottom: 1.5rem;
  padding: 0;
}

/* Layout de Vista Dual (Izquierda detalle, Derecha documentos) */
.dual-view-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .dual-view-layout {
    grid-template-columns: 1fr;
  }
}

.detail-card, .documents-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.detail-header h1, .documents-header h3 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.documents-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.meta {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.badge {
  font-size: 0.8rem;
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  background: rgba(66, 184, 131, 0.15);
  color: #42b883;
}

.detail-body p {
  line-height: 1.6;
  opacity: 0.9;
}

/* Estilos específicos para la sección de feedback */
.feedback-section {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(66, 184, 131, 0.08);
  border: 1px solid rgba(66, 184, 131, 0.2);
  border-radius: 8px;
}

.feedback-section h3 {
  font-size: 0.95rem;
  color: #42b883;
  margin-top: 0;
  margin-bottom: 0.5rem;
}

.feedback-text {
  margin: 0;
  font-size: 0.95rem;
}

.detail-footer {
  margin-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 1rem;
  opacity: 0.5;
}

/* Listado de documentos */
.document-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.document-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.07);
  padding: 0.75rem 1rem;
  border-radius: 8px;
}

.doc-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin-right: 1rem;
}

.doc-name {
  font-size: 0.95rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-date {
  font-size: 0.75rem;
  opacity: 0.5;
}

.btn-action {
  background: rgba(66, 184, 131, 0.15);
  color: #42b883;
  border: 1px solid rgba(66, 184, 131, 0.3);
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.2s;
}

.btn-action:hover {
  background: rgba(66, 184, 131, 0.3);
}

.state-message {
  text-align: center;
  padding: 3rem;
  opacity: 0.7;
}

.state-message-sm {
  text-align: center;
  padding: 1.5rem;
  opacity: 0.6;
  font-size: 0.9rem;
}

.state-message.error, .state-message-sm.error {
  color: #ff5252;
  opacity: 1;
}
</style>