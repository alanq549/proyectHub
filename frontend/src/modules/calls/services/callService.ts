// src/modules/calls/services/callService.ts

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

export interface CallRequirement {
  id: number
  call_id: number
  title: string
  description?: string
  is_required: boolean
}

export interface CallParticipant {
  id: number
  call_id: number
  user_id: number
  user_email?: string
  user_name?: string
  status: 'REGISTERED' | 'SUBMITTED' | 'IN_REVIEW' | 'APPROVED' | 'REJECTED'
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
    const response = await api.post<{ message: string; data: Call }>(
      '/calls/',
      payload
    )

    return response.data.data
  },


  async updateCall(
    id: number,
    payload: UpdateCallPayload
  ): Promise<Call> {

    const response = await api.put<{ message: string; data: Call }>(
      `/calls/${id}`,
      payload
    )

    return response.data.data
  },


  async deleteCall(id: number): Promise<void> {
    await api.delete(`/calls/${id}`)
  },

  // Inscribir al usuario autenticado a la convocatoria
  async joinCall(callId: number) {
    const response = await api.post(`/calls/${callId}/join`)
    return response.data
  },

  // Añadir un requisito a la convocatoria (Solo Admin)
  async addRequirement(callId: number, data: { title: string; description?: string; is_required?: boolean }) {
    const response = await api.post(`/calls/${callId}/requirements`, data)
    return response.data.data
  },

  // Cambiar el dictamen de una postulación (Solo Admin)
  async updateParticipantStatus(participantId: number, status: string) {
    const response = await api.patch(`/calls/participants/${participantId}/status`, { status })
    return response.data.data
  }
}