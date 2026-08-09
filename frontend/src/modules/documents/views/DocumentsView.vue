<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { documentService, type DocumentModel } from '../services/documentService'

const documents = ref<DocumentModel[]>([])
const loading = ref(true)

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

onMounted(fetchAllDocuments)
</script>

<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">Mis Documentos</h1>
    <div v-if="loading" class="text-gray-500">Cargando documentos...</div>
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
      <table class="w-full text-left text-sm">
        <thead>
          <tr class="border-b text-gray-500">
            <th class="py-2">Nombre</th>
            <th class="py-2">MIME Type</th>
            <th class="py-2">Tamaño</th>
            <th class="py-2">Fecha de creación</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="doc in documents" :key="doc.id" class="border-b hover:bg-gray-50">
            <td class="py-3 font-medium">{{ doc.original_filename }}</td>
            <td class="py-3 text-gray-500">{{ doc.mime_type }}</td>
            <td class="py-3">{{ (doc.file_size / 1024).toFixed(1) }} KB</td>
            <td class="py-3">{{ new Date(doc.created_at).toLocaleDateString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>