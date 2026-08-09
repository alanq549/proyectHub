// src/modules/documents/services/documentService.ts
import api from '@/api/axios'

export interface DocumentModel {
  id: number
  filename: string
  original_filename: string
  file_path: string
  mime_type: string
  file_size: number
  status: string
  user_id: number
  project_id?: number
  call_id?: number
  created_at: string
}


export const documentService = {
  async getDocuments(params?: { project_id?: number; call_id?: number }): Promise<DocumentModel[]> {
    // Añadir el slash final '/' evita el redirect 308
    const response = await api.get('/documents/', { params })
    return response.data.data
  },

  async uploadDocument(formData: FormData): Promise<DocumentModel> {
    const response = await api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data.data
  },

  async downloadDocument(id: number, fileName: string): Promise<void> {
    const response = await api.get(`/documents/${id}/download`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    link.remove()
  },

  async deleteDocument(id: number): Promise<void> {
    await api.delete(`/documents/${id}`)
  }
}