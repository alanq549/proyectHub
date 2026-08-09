import api from '@/api/axios'

export interface ActivityLogModel {
  id: number
  user_id: number
  user_email?: string // Opcional si tu to_dict lo incluye
  action: string
  description?: string
  entity_type?: string
  entity_id?: number
  details?: string
  created_at: string
}

export const historyService = {
  async getHistory(params?: { entity_type?: string; entity_id?: number; limit?: number }): Promise<ActivityLogModel[]> {
    const response = await api.get('/history/', { params })
    return response.data.data
  }
}