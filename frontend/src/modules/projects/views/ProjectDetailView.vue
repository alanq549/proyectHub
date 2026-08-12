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
const loadingDocs = ref(true)
const error = ref<string | null>(null)

// Helper para leer el mensaje de error de una respuesta Axios sin usar 'any'
function extractErrorMessage(err: unknown, fallback: string): string {
  const axiosErr = err as { response?: { data?: { message?: string } } }
  return axiosErr?.response?.data?.message || fallback
}

const fetchProjectDetails = async () => {
  const id = route.params.id as string
  if (!id) return

  loading.value = true
  error.value = null
  try {
    project.value = await projectService.getById(id)
  } catch (err: unknown) {
    error.value = extractErrorMessage(err, 'Error al cargar los detalles del proyecto.')
  } finally {
    loading.value = false
  }
}

const fetchProjectDocuments = async () => {
  const id = route.params.id as string
  if (!id) return

  loadingDocs.value = true
  try {
    documents.value = await documentService.getDocuments({ project_id: Number(id) })
  } catch (err: unknown) {
    console.error('Error al cargar documentos del proyecto:', err)
  } finally {
    loadingDocs.value = false
  }
}

const handleDownloadDocument = async (doc: DocumentModel) => {
  try {
    await documentService.downloadDocument(doc.id, doc.original_filename || doc.filename)
  } catch (err) {
    console.error('Error al descargar el documento:', err)
    alert('Error al intentar descargar el documento.')
  }
}

const goBack = () => {
  router.push({ name: 'projects-list' })
}

onMounted(() => {
  fetchProjectDetails()
  fetchProjectDocuments()
})
</script>

<template>
  <div class="project-detail-container">
    <div class="header-actions">
      <button @click="goBack" class="back-btn">
        &larr; Volver a proyectos
      </button>
    </div>

    <div v-if="loading" class="state-message">Cargando detalles...</div>

    <div v-else-if="error" class="state-message error">{{ error }}</div>

    <div v-else-if="!project" class="state-message">
      Proyecto no encontrado.
    </div>

    <div v-else class="project-detail-card">
      <header class="detail-header">
        <div class="title-group">
          <h1>{{ project.title }}</h1>
          <span v-if="project.category" class="badge">{{ project.category }}</span>
        </div>
        <span v-if="project.status" class="status-tag" :class="project.status.toLowerCase()">
          {{ project.status }}
        </span>
      </header>

      <section class="detail-content">
        <h3>Descripción</h3>
        <p>{{ project.description || 'Sin descripción provista.' }}</p>
      </section>

      <!-- SECCIÓN DE DOCUMENTOS -->
      <section class="documents-section">
        <h3>Documentos asociados</h3>
        
        <div v-if="loadingDocs" class="docs-state">
          Cargando documentos...
        </div>
        
        <div v-else-if="documents.length === 0" class="docs-empty">
          <span class="material-symbols-outlined icon-empty">folder_off</span>
          <p>Este proyecto no tiene documentos asociados.</p>
        </div>
        
        <div v-else class="documents-list">
          <div v-for="doc in documents" :key="doc.id" class="document-item">
            <div class="doc-info">
              <div class="doc-icon">
                <span class="material-symbols-outlined">description</span>
              </div>
              <div class="doc-details">
                <p class="doc-name">{{ doc.original_filename || doc.filename }}</p>
                <div class="doc-meta">
                  <span>{{ (doc.file_size / 1024).toFixed(1) }} KB</span>
                  <span class="separator">•</span>
                  <span>{{ new Date(doc.created_at).toLocaleDateString('es-MX') }}</span>
                </div>
              </div>
            </div>
            
            <button class="download-btn" @click="handleDownloadDocument(doc)" title="Descargar documento">
              <span class="material-symbols-outlined">download</span>
            </button>
          </div>
        </div>
      </section>

      <footer class="detail-footer" v-if="project.created_at">
        <p class="date">Registrado el: {{ new Date(project.created_at).toLocaleDateString('es-MX') }}</p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.project-detail-container {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
  background-color: var(--background, #f7f9fb);
  min-height: calc(100vh - 100px);
}

.header-actions {
  margin-bottom: 2rem;
}

.back-btn {
  background: none;
  border: none;
  color: var(--ph-navy, #10192B);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  transition: opacity 0.2s;
  padding: 0;
}

.back-btn:hover {
  opacity: 0.7;
}

.project-detail-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eaeaea;
}

.title-group h1 {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-weight: 700;
  color: var(--ph-navy, #10192B);
  margin: 0 0 0.75rem 0;
  font-size: 2rem;
}

.badge {
  font-size: 0.85rem;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  background: rgba(66, 184, 131, 0.15);
  color: #42b883;
  font-weight: 600;
}

.status-tag {
  font-size: 0.85rem;
  padding: 0.3rem 0.75rem;
  border-radius: 6px;
  font-weight: 600;
  background: #f0f0f0;
  color: #666;
  text-transform: capitalize;
}

.status-tag.approved {
  background: rgba(66, 184, 131, 0.15);
  color: #42b883;
}

.status-tag.rejected {
  background: rgba(255, 82, 82, 0.15);
  color: #ff5252;
}

.status-tag.draft {
  background: rgba(201, 151, 74, 0.15);
  color: #C9974A;
}

.status-tag.submitted {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.detail-content h3 {
  font-size: 1.2rem;
  color: var(--ph-navy, #10192B);
  margin-bottom: 1rem;
}

.detail-content p {
  color: var(--on-surface-variant, #45464d);
  line-height: 1.6;
  font-size: 1.05rem;
  white-space: pre-wrap;
}

/* Documentos */
.documents-section {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #eaeaea;
}

.documents-section h3 {
  font-size: 1.2rem;
  color: var(--ph-navy, #10192B);
  margin-bottom: 1.5rem;
}

.docs-state {
  color: #888;
  font-size: 0.95rem;
  font-style: italic;
}

.docs-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: #fafafa;
  border-radius: 12px;
  border: 1px dashed #dcdcdc;
  color: #888;
}

.icon-empty {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ccc;
}

.documents-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.document-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: #fff;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  transition: all 0.2s ease;
}

.document-item:hover {
  border-color: rgba(66, 184, 131, 0.4);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.doc-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 0;
}

.doc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: rgba(66, 184, 131, 0.1);
  color: #42b883;
}

.doc-details {
  min-width: 0;
}

.doc-name {
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--ph-navy, #10192B);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.doc-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: #888;
}

.separator {
  color: #dcdcdc;
}

.download-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.download-btn:hover {
  background: rgba(66, 184, 131, 0.1);
  color: #42b883;
}

.detail-footer {
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eaeaea;
}

.date {
  color: #888;
  font-size: 0.9rem;
}

.state-message {
  text-align: center;
  padding: 3rem;
  color: var(--on-surface-variant, #45464d);
  font-size: 1.1rem;
}

.state-message.error {
  color: var(--app-error, #ba1a1a);
}
</style>
