// src/modules/projects/services/projectService.ts
import api from '@/api/axios'

export interface Project {
  id: number
  title: string
  description: string
  category?: string
  status?: string
  created_at?: string
  updated_at?: string
  [key: string]: any
}

export interface ProjectsResponse {
  data: Project[]
  message?: string
}

export interface ProjectResponse {
  data: Project
  message?: string
}

export const projectService = {
  async getAll(params?: Record<string, any>): Promise<Project[]> {
    const response = await api.get<ProjectsResponse>('/projects/', { params })
    return response.data.data
  },

  async getById(id: number | string): Promise<Project> {
    const response = await api.get<ProjectResponse>(`/projects/${id}`)
    return response.data.data
  },

  async create(payload: Partial<Project>): Promise<Project> {
    const response = await api.post<ProjectResponse>('/projects/', payload)
    return response.data.data
  },

  async update(id: number | string, payload: Partial<Project>): Promise<Project> {
    const response = await api.put<ProjectResponse>(`/projects/${id}`, payload)
    return response.data.data
  },

  async delete(id: number | string): Promise<void> {
    await api.delete(`/projects/${id}`)
  }
}