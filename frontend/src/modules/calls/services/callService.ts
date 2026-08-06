import api from '@/api/axios'

export interface Call {
  id: number
  title: string
  description?: string
  start_date: string
  end_date: string
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface CreateCallPayload {
  title: string
  description?: string
  start_date: string
  end_date: string
  is_active?: boolean
}

export interface UpdateCallPayload {
  title?: string
  description?: string
  start_date?: string
  end_date?: string
  is_active?: boolean
}

export const callService = {
  async getCalls(): Promise<Call[]> {
    const response = await api.get<{ data: Call[] }>('/calls/')
    return response.data.data
  },

  async getCallById(id: number): Promise<Call> {
    const response = await api.get<{ data: Call }>(`/calls/${id}`)
    return response.data.data
  },

  async createCall(payload: CreateCallPayload): Promise<Call> {
    const response = await api.post<{ message: string; data: Call }>('/calls/', payload)
    return response.data.data
  },

  async updateCall(id: number, payload: UpdateCallPayload): Promise<Call> {
    const response = await api.put<{ message: string; data: Call }>(`/calls/${id}`, payload)
    return response.data.data
  },

  async deleteCall(id: number): Promise<void> {
    await api.delete(`/calls/${id}`)
  }
}