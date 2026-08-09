<script setup lang="ts">
import { ref } from 'vue'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'

const props = defineProps<{
  callId: number
  projectId?: number
  documents: DocumentModel[]
}>()

const emit = defineEmits(['refresh'])

const uploading = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const files = target.files
  
  if (!files || files.length === 0 || !files[0]) return

  const file = files[0]
  const formData = new FormData()
  formData.append('file', file)
  formData.append('call_id', props.callId.toString())
  
  if (props.projectId) {
    formData.append('project_id', props.projectId.toString())
  }

  try {
    uploading.value = true
    await documentService.uploadDocument(formData)
    emit('refresh')
  } catch (error) {
    console.error('Error al subir documento:', error)
  } finally {
    uploading.value = false
    if (fileInput.value) fileInput.value.value = ''
  }
}

const downloadFile = (doc: DocumentModel) => {
  documentService.downloadDocument(doc.id, doc.original_filename)
}

const deleteFile = async (id: number) => {
  if (!confirm('¿Seguro que deseas eliminar este documento?')) return
  try {
    await documentService.deleteDocument(id)
    emit('refresh')
  } catch (error) {
    console.error('Error al eliminar documento:', error)
  }
}
</script>

<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <h3 class="text-lg font-semibold text-gray-800">Documentos</h3>
      <div>
        <input 
          type="file" 
          ref="fileInput" 
          class="hidden" 
          @change="handleFileUpload" 
        />
        <button 
          @click="fileInput?.click()" 
          :disabled="uploading"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {{ uploading ? 'Subiendo...' : 'Subir Documento' }}
        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg border border-gray-200 overflow-hidden shadow-sm">
      <table class="w-full text-left text-sm text-gray-600">
        <thead class="bg-gray-50 border-b border-gray-200 text-gray-700 font-medium">
          <tr>
            <th class="py-3 px-4">Nombre</th>
            <th class="py-3 px-4">MIME Type</th>
            <th class="py-3 px-4">Tamaño</th>
            <th class="py-3 px-4">Fecha de creación</th>
            <th class="py-3 px-4 text-right">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="doc in documents" :key="doc.id" class="hover:bg-gray-50/50">
            <td class="py-3 px-4 font-medium text-gray-900">{{ doc.original_filename }}</td>
            <td class="py-3 px-4 text-gray-500">{{ doc.mime_type }}</td>
            <td class="py-3 px-4">{{ (doc.file_size / 1024).toFixed(1) }} KB</td>
            <td class="py-3 px-4">{{ new Date(doc.created_at).toLocaleDateString() }}</td>
            <td class="py-3 px-4 text-right space-x-2">
              <button 
                @click="downloadFile(doc)" 
                class="text-indigo-600 hover:text-indigo-800 font-medium"
              >
                Descargar
              </button>
              <button 
                @click="deleteFile(doc.id)" 
                class="text-red-600 hover:text-red-800 font-medium"
              >
                Eliminar
              </button>
            </td>
          </tr>
          <tr v-if="documents.length === 0">
            <td colspan="5" class="text-center py-6 text-gray-400">
              No hay documentos registrados.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>