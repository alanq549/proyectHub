<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { documentService, type DocumentModel } from '../services/documentService'
import AppCard from '@/shared/components/AppCard.vue'
import AppBadge from '@/shared/components/AppBadge.vue'
import AppButton from '@/shared/components/AppButton.vue'

const documents = ref<DocumentModel[]>([])
const loading = ref(true)
const downloadingId = ref<number | null>(null)

const fetchAllDocuments = async () => {
  try {
    loading.value = true
    documents.value = await documentService.getDocuments()
  } catch (error) {
    console.error('Error al cargar documentos:', error)
  } finally {
    loading.value = false
  }
}

const handleDownload = async (doc: DocumentModel) => {
  try {
    downloadingId.value = doc.id

    await documentService.downloadDocument(
      doc.id,
      doc.original_filename || doc.filename
    )
  } catch (error) {
    console.error('Error al descargar documento:', error)
  } finally {
    downloadingId.value = null
  }
}

const formatFileSize = (bytes: number) => {
  if (!bytes) return '0 KB'

  if (bytes < 1024) {
    return `${bytes} B`
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`
  }

  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('es-MX', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const getFileIcon = (mimeType?: string) => {
  if (!mimeType) return 'description'

  if (mimeType.includes('pdf')) {
    return 'picture_as_pdf'
  }

  if (
    mimeType.includes('word') ||
    mimeType.includes('document')
  ) {
    return 'article'
  }

  if (
    mimeType.includes('excel') ||
    mimeType.includes('spreadsheet')
  ) {
    return 'table_chart'
  }

  if (mimeType.includes('image')) {
    return 'image'
  }

  if (
    mimeType.includes('zip') ||
    mimeType.includes('rar') ||
    mimeType.includes('compressed')
  ) {
    return 'folder_zip'
  }

  return 'description'
}

const getFileType = (mimeType?: string) => {
  if (!mimeType) return 'Archivo'

  if (mimeType.includes('pdf')) return 'PDF'
  if (mimeType.includes('word')) return 'DOCX'
  if (mimeType.includes('excel')) return 'XLSX'
  if (mimeType.includes('image')) return 'Imagen'
  if (mimeType.includes('zip')) return 'ZIP'

  return mimeType.split('/').pop()?.toUpperCase() || 'Archivo'
}

onMounted(fetchAllDocuments)
</script>

<template>
  <section class="tw-space-y-6">

    <!-- Header -->
    <div>
      <div class="tw-flex tw-items-center tw-gap-2 tw-mb-1.5">
        <span class="tw-h-px tw-w-6 tw-bg-primary/60"></span>

        <span
          class="tw-text-[11px] tw-font-semibold tw-tracking-[0.18em] tw-uppercase tw-text-primary"
        >
          Archivos
        </span>
      </div>

      <div class="tw-flex tw-items-center tw-gap-3">
        <div
          class="tw-w-10 tw-h-10 tw-rounded-xl tw-bg-primary/10 tw-text-primary tw-flex tw-items-center tw-justify-center"
        >
          <span class="material-symbols-outlined notranslate tw-text-xl">
            folder
          </span>
        </div>

        <div>
          <h1 class="tw-text-xl tw-font-bold tw-text-on-surface">
            Mis Documentos
          </h1>

          <p class="tw-text-sm tw-text-on-surface-variant">
            Consulta y descarga los documentos asociados a tus proyectos.
          </p>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <AppCard
      v-if="loading"
      padding="md"
      variant="glass"
      class="tw-border tw-border-outline-variant/60"
    >
      <div class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-py-12">
        <span
          class="material-symbols-outlined notranslate tw-text-3xl tw-text-primary tw-animate-spin"
        >
          progress_activity
        </span>

        <p class="tw-text-sm tw-text-on-surface-variant tw-mt-3">
          Cargando documentos...
        </p>
      </div>
    </AppCard>

    <!-- Contenido -->
    <AppCard
      v-else
      padding="md"
      variant="glass"
      class="tw-border tw-border-outline-variant/60 tw-bg-surface-container/60 tw-backdrop-blur-xl"
    >

      <!-- Header de tabla -->
      <div
        class="tw-flex tw-items-center tw-justify-between tw-gap-4 tw-mb-5"
      >
        <div>
          <h2 class="tw-text-base tw-font-semibold tw-text-on-surface">
            Documentos disponibles
          </h2>

          <p class="tw-text-xs tw-text-on-surface-variant tw-mt-0.5">
            {{ documents.length }}
            {{ documents.length === 1 ? 'documento registrado' : 'documentos registrados' }}
          </p>
        </div>

        <div
          class="tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-1.5 tw-rounded-lg tw-bg-surface-container-low tw-border tw-border-outline-variant/60"
        >
          <span
            class="material-symbols-outlined notranslate tw-text-sm tw-text-primary"
          >
            folder_open
          </span>

          <span class="tw-text-xs tw-font-medium tw-text-on-surface-variant">
            {{ documents.length }}
          </span>
        </div>
      </div>

      <!-- Estado vacío -->
      <div
        v-if="documents.length === 0"
        class="tw-flex tw-flex-col tw-items-center tw-justify-center tw-text-center tw-py-14 tw-rounded-2xl tw-border-2 tw-border-dashed tw-border-outline-variant/60 tw-bg-surface-container-low/40"
      >
        <div
          class="tw-w-14 tw-h-14 tw-rounded-2xl tw-bg-surface-container tw-flex tw-items-center tw-justify-center tw-mb-4"
        >
          <span
            class="material-symbols-outlined notranslate tw-text-3xl tw-text-outline"
          >
            folder_off
          </span>
        </div>

        <h3 class="tw-text-sm tw-font-bold tw-text-on-surface">
          No tienes documentos
        </h3>

        <p
          class="tw-text-xs tw-text-on-surface-variant tw-mt-1 tw-max-w-sm"
        >
          Los documentos que adjuntes a tus proyectos aparecerán aquí.
        </p>
      </div>

      <!-- Tabla -->
      <div
        v-else
        class="tw-overflow-x-auto tw-rounded-2xl tw-border tw-border-outline-variant/60"
      >
        <table class="tw-w-full tw-align-middle">

          <thead
            class="tw-bg-surface-container-low/60 tw-border-b tw-border-outline-variant"
          >
            <tr>
              <th
                class="tw-px-4 tw-py-3.5 tw-text-left tw-text-[11px] tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider"
              >
                Documento
              </th>

              <th
                class="tw-px-4 tw-py-3.5 tw-text-left tw-text-[11px] tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider"
              >
                Tipo
              </th>

              <th
                class="tw-px-4 tw-py-3.5 tw-text-left tw-text-[11px] tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider"
              >
                Tamaño
              </th>

              <th
                class="tw-px-4 tw-py-3.5 tw-text-left tw-text-[11px] tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider"
              >
                Fecha
              </th>

              <th
                class="tw-px-4 tw-py-3.5 tw-text-right tw-text-[11px] tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider"
              >
                Acción
              </th>
            </tr>
          </thead>

          <tbody
            class="tw-divide-y tw-divide-outline-variant/50"
          >
            <tr
              v-for="doc in documents"
              :key="doc.id"
              class="tw-group hover:tw-bg-primary/[0.035] tw-transition-colors"
            >

              <!-- Documento -->
              <td class="tw-px-4 tw-py-3.5">
                <div class="tw-flex tw-items-center tw-gap-3 tw-min-w-[240px]">

                  <div
                    class="tw-w-10 tw-h-10 tw-shrink-0 tw-rounded-xl tw-bg-primary/10 tw-text-primary tw-flex tw-items-center tw-justify-center tw-transition-colors group-hover:tw-bg-primary group-hover:tw-text-on-primary"
                  >
                    <span class="material-symbols-outlined notranslate tw-text-xl">
                      {{ getFileIcon(doc.mime_type) }}
                    </span>
                  </div>

                  <div class="tw-min-w-0">
                    <p
                      class="tw-text-sm tw-font-semibold tw-text-on-surface tw-truncate tw-max-w-[320px]"
                      :title="doc.original_filename || doc.filename"
                    >
                      {{ doc.original_filename || doc.filename }}
                    </p>

                    <p
                      class="tw-text-[11px] tw-text-on-surface-variant tw-mt-0.5"
                    >
                      Archivo #{{ doc.id }}
                    </p>
                  </div>
                </div>
              </td>

              <!-- Tipo -->
              <td class="tw-px-4 tw-py-3.5">
                <AppBadge variant="neutral">
                  {{ getFileType(doc.mime_type) }}
                </AppBadge>
              </td>

              <!-- Tamaño -->
              <td
                class="tw-px-4 tw-py-3.5 tw-text-xs tw-font-medium tw-text-on-surface-variant"
              >
                {{ formatFileSize(doc.file_size) }}
              </td>

              <!-- Fecha -->
              <td class="tw-px-4 tw-py-3.5">
                <div class="tw-flex tw-items-center tw-gap-1.5">
                  <span
                    class="material-symbols-outlined notranslate tw-text-sm tw-text-outline"
                  >
                    calendar_today
                  </span>

                  <span
                    class="tw-text-xs tw-text-on-surface-variant tw-whitespace-nowrap"
                  >
                    {{ formatDate(doc.created_at) }}
                  </span>
                </div>
              </td>

              <!-- Acción -->
              <td class="tw-px-4 tw-py-3.5 tw-text-right">
                <AppButton
                  variant="ghost"
                  size="sm"
                  icon="download"
                  :loading="downloadingId === doc.id"
                  @click="handleDownload(doc)"
                >
                  <span class="tw-hidden sm:tw-inline">
                    Descargar
                  </span>
                </AppButton>
              </td>

            </tr>
          </tbody>
        </table>
      </div>

    </AppCard>
  </section>
</template>