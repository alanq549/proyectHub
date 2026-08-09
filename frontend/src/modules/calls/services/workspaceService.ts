//src/modules/calls/services/workspaceService.ts
import api from '@/api/axios'
import type { Call } from './callService'

export interface CallRequirement {
  id: number
  call_id: number
  title: string
  description?: string | null
  is_required: boolean
}

export interface CallWorkspaceStats {
  documents_uploaded: number
  progress: number
}

export interface CallWorkspace {
  call: Call
  requirements: CallRequirement[]
  project: null
  documents: []
  tracking: []
  stats: CallWorkspaceStats
  participant_status?: string | null  // <-- Agregar esta línea

}

export const workspaceService = {
  async getWorkspace(id: number): Promise<CallWorkspace> {
    const response = await api.get<{ data: CallWorkspace }>(
      `/calls/${id}/workspace`
    )

    return response.data.data
  }
}
