<!-- src/modules/calls/workspace/WorkspaceHeader.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { Call } from '../services/callService'
import type { CallWorkspace } from '../services/workspaceService'
import { useAuthStore } from '@/stores/authStore'
import AppBadge from '@/shared/components/AppBadge.vue'

const props = defineProps<{
  call: Call
  workspace: CallWorkspace
}>()

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isRegistered = computed(() => {
  return props.workspace.participant_status && props.workspace.participant_status !== 'NOT_REGISTERED'
})

const isAdmin = computed(() => authStore.user?.role === 'admin')

const tabs = computed(() => {
  const allTabs = [
    {
      name: 'information',
      label: 'Información',
      icon: 'info',
      routeName: 'call-information',
      visible: true
    },
    {
      name: 'project',
      label: 'Mi proyecto',
      icon: 'folder',
      routeName: 'call-project',
      visible: isRegistered.value
    },
    {
      name: 'submissions',
      label: 'Postulaciones / Inscritos',
      icon: 'groups',
      routeName: 'call-submissions',
      visible: isAdmin.value
    },
    {
      name: 'tracking',
      label: 'Seguimiento',
      icon: 'timeline',
      routeName: 'call-tracking',
      visible: isRegistered.value
    }
  ]

  return allTabs.filter(tab => tab.visible)
})

function isActive(routeName: string): boolean {
  return route.name === routeName
}

function go(routeName: string) {
  router.push({
    name: routeName,
    params: { id: route.params.id }
  })
}
</script>

<template>
  <div class="app-card-glass-xl tw-space-y-6">
    <!-- Parte Superior: Info principal y Estado -->
    <div class="tw-flex tw-flex-col tw-gap-4 sm:tw-flex-row sm:tw-items-center sm:tw-justify-between">
      <div class="tw-flex tw-items-center tw-gap-4">
        <!-- Icono contenedor con tono de Tinta Académica y acento de latón -->
        <div class="tw-flex tw-h-14 tw-w-14 tw-shrink-0 tw-items-center tw-justify-center tw-rounded-2xl tw-bg-[var(--app-primary)] tw-text-white tw-shadow-md">
          <span class="material-symbols-outlined notranslate tw-text-3xl">
            campaign
          </span>
        </div>

        <div>
          <!-- Título principal h1 -->
          <h1 class="tw-text-2xl tw-font-bold tw-text-[var(--app-primary)]">
            {{ call.title }}
          </h1>

          <!-- Texto secundario -->
          <p class="tw-text-sm tw-text-[var(--app-secondary)]">
            Convocatoria académica
          </p>
        </div>
      </div>

      <!-- Estado / Badge -->
      <div class="tw-flex tw-items-center">
        <AppBadge
          :variant="call.is_active ? 'success' : 'neutral'"
          :dot="true"
        >
          {{ call.is_active ? 'Abierta' : 'Cerrada' }}
        </AppBadge>
      </div>
    </div>

    <!-- Divisor sutil -->
    <div class="tw-border-t tw-border-[var(--app-outline-variant)]/40"></div>

    <!-- Pestañas integradas con la paleta Tinta Académica (Primary/Surface) -->
    <nav class="tw-flex tw-gap-2 tw-overflow-x-auto tw-no-scrollbar" aria-label="Tabs">
      <button
        v-for="tab in tabs"
        :key="tab.name"
        type="button"
        @click="go(tab.routeName)"
        :class="[
          'tw-group tw-relative tw-flex tw-items-center tw-gap-2.5 tw-px-4 tw-py-2.5 tw-text-sm tw-font-medium tw-transition-all tw-duration-200 tw-rounded-xl tw-shrink-0',
          'focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--app-primary)]/20',
          isActive(tab.routeName)
            ? 'tw-bg-[var(--app-primary)] tw-text-[var(--app-on-primary)] tw-shadow-sm'
            : 'tw-text-[var(--app-on-surface-variant)] hover:tw-text-[var(--app-on-surface)] hover:tw-bg-[var(--app-surface-container-high)]/60'
        ]"
      >
        <div
          :class="[
            'tw-flex tw-h-6 tw-w-6 tw-items-center tw-justify-center tw-rounded-lg tw-transition-colors',
            isActive(tab.routeName)
              ? 'tw-bg-white/20 tw-text-[var(--app-on-primary)]'
              : 'tw-bg-[var(--app-surface-container)] tw-text-[var(--app-on-surface-variant)] group-hover:tw-text-[var(--app-on-surface)]'
          ]"
        >
          <span class="material-symbols-outlined notranslate tw-text-sm">
            {{ tab.icon }}
          </span>
        </div>

        <span class="tw-whitespace-nowrap">{{ tab.label }}</span>
      </button>
    </nav>
  </div>
</template>