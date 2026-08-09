// src/modules/calls/stores/workspaceStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  workspaceService,
  type CallWorkspace,
  type CallRequirement
} from '../services/workspaceService'

const CACHE_PREFIX = 'projecthub.workspace.v1.'

interface CachedWorkspace {
  workspace: CallWorkspace
  timestamp: number
}

function readCachedWorkspace(callId: number): CallWorkspace | null {
  try {
    const raw = localStorage.getItem(`${CACHE_PREFIX}${callId}`)
    if (!raw) return null
    const parsed = JSON.parse(raw) as CachedWorkspace
    return parsed.workspace ?? null
  } catch {
    return null
  }
}

function persistWorkspace(callId: number, workspace: CallWorkspace) {
  try {
    const data: CachedWorkspace = { workspace, timestamp: Date.now() }
    localStorage.setItem(`${CACHE_PREFIX}${callId}`, JSON.stringify(data))
  } catch {
    // Manejo de cuota superada en localStorage
  }
}

export function clearWorkspaceCache(callId: number) {
  try {
    localStorage.removeItem(`${CACHE_PREFIX}${callId}`)
  } catch {
    // Ignorar si falla
  }
}

export const useWorkspaceStore = defineStore('workspace', () => {
  const currentWorkspace = ref<CallWorkspace | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  let activeRequest: Promise<CallWorkspace> | null = null

  async function fetchWorkspace(callId: number, forceRefresh = false): Promise<CallWorkspace> {
    // Si ya coincide el ID en memoria y no pedimos refresh
    if (!forceRefresh && currentWorkspace.value && currentWorkspace.value.call.id === callId) {
      return currentWorkspace.value
    }

    // Intentar leer de caché si no es forzado
    if (!forceRefresh) {
      const cached = readCachedWorkspace(callId)
      if (cached) {
        currentWorkspace.value = cached
        return cached
      }
    }

    if (activeRequest) return activeRequest

    loading.value = true
    error.value = null

    activeRequest = workspaceService
      .getWorkspace(callId)
      .then((data) => {
        currentWorkspace.value = data
        persistWorkspace(callId, data)
        return data
      })
      .catch((err) => {
        error.value = 'No se pudo cargar el espacio de trabajo.'
        throw err
      })
      .finally(() => {
        loading.value = false
        activeRequest = null
      })

    return activeRequest
  }

  // Actualizar caché de manera local tras acciones (Inscripción, Modificación de requisitos)
  function setWorkspace(data: CallWorkspace) {
    currentWorkspace.value = data
    persistWorkspace(data.call.id, data)
  }

  function clearCurrent() {
    currentWorkspace.value = null
  }

  return {
    currentWorkspace,
    loading,
    error,
    fetchWorkspace,
    setWorkspace,
    clearCurrent
  }
})