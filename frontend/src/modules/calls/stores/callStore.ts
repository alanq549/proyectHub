// src/modules/calls/stores/callStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  callService,
  type Call,
  type CreateCallPayload,
  type UpdateCallPayload
} from '../services/callService'

const CACHE_KEY = 'projecthub.calls.v1'

interface PersistedCallsCache {
  calls: Call[]
  isLoaded: true
}

function readCachedCalls(): Call[] | null {
  try {
    const cachedValue = localStorage.getItem(CACHE_KEY)

    if (!cachedValue) return null

    const cache = JSON.parse(cachedValue) as PersistedCallsCache
    return cache.isLoaded && Array.isArray(cache.calls) ? cache.calls : null
  } catch {
    return null
  }
}

function persistCalls(calls: Call[]) {
  try {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ calls, isLoaded: true }))
  } catch {
    // The in-memory cache remains available when browser storage is unavailable.
  }
}


export const useCallStore = defineStore('calls', () => {

  const cachedCalls = readCachedCalls()
  const calls = ref<Call[]>(cachedCalls ?? [])
  const loading = ref(false)
  const isLoaded = ref(cachedCalls !== null)
  let activeRequest: Promise<void> | null = null


  function fetchCalls(forceRefresh = false): Promise<void> {

    // 🟢 CACHE
    if (activeRequest) return activeRequest

    // Show the persisted value immediately, then revalidate it. A seed or
    // change from another browser cannot otherwise invalidate localStorage.
    loading.value = forceRefresh || !isLoaded.value
    activeRequest = callService
      .getCalls()
      .then((receivedCalls) => {
        calls.value = receivedCalls
        isLoaded.value = true
        persistCalls(receivedCalls)
      })
      .finally(() => {
        loading.value = false
        activeRequest = null
      })

    return activeRequest
  }


  async function createCall(payload: CreateCallPayload) {

    const newCall = await callService.createCall(payload)

    // 🟢 actualizar cache
    calls.value.push(newCall)
    isLoaded.value = true
    persistCalls(calls.value)

    return newCall
  }

  async function updateCall(
  id: number,
  payload: UpdateCallPayload
) {

  const updatedCall = await callService.updateCall(id, payload)

  const index = calls.value.findIndex(
    call => call.id === id
  )

  if (index !== -1) {
    calls.value[index] = updatedCall
    persistCalls(calls.value)
  }

  return updatedCall
}


  async function deleteCall(id: number) {

    await callService.deleteCall(id)

    // 🟢 actualizar cache
    calls.value = calls.value.filter(
      call => call.id !== id
    )
    persistCalls(calls.value)
  }


  return {
    calls,
    loading,
    isLoaded,
    fetchCalls,
    createCall,
    updateCall,
    deleteCall
  }
})
