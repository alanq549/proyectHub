<!-- src/modules/calls/workspace/WorkspaceTabs.vue -->
<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { CallWorkspace } from '../services/workspaceService'
import { useAuthStore } from '@/stores/authStore'

const props = defineProps<{
  workspace: CallWorkspace
}>()

const router = useRouter()
const route = useRoute()

const isRegistered = computed(() => {
  return props.workspace.participant_status && props.workspace.participant_status !== 'NOT_REGISTERED'
})

const authStore = useAuthStore() 
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
  <div class="tw-border-b tw-border-[var(--app-outline-variant)]/40 tw-px-2 sm:tw-px-6">
    <nav class="tw-flex tw-gap-2 tw-overflow-x-auto tw-no-scrollbar" aria-label="Tabs">
      <button
        v-for="tab in tabs"
        :key="tab.name"
        type="button"
        @click="go(tab.routeName)"
        :class="[
          'tw-group tw-relative tw-flex tw-items-center tw-gap-2.5 tw-px-4 tw-py-3 tw-text-sm tw-font-medium tw-transition-all tw-duration-200 tw-shrink-0 tw-rounded-t-xl',
          'focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--app-accent-brass)]/30',
          isActive(tab.routeName)
            ? 'tw-bg-[var(--app-primary)] tw-text-[var(--app-on-primary)] tw-shadow-sm'
            : 'tw-text-[var(--app-on-surface-variant)] hover:tw-text-[var(--app-on-surface)] hover:tw-bg-[var(--app-surface-container-high)]/60'
        ]"
      >
        <!-- Contenedor del ícono: usa tono latón/naranja cuando está activo para dar el toque cálido de acento -->
        <div
          :class="[
            'tw-flex tw-h-7 tw-w-7 tw-items-center tw-justify-center tw-rounded-lg tw-transition-colors',
            isActive(tab.routeName)
              ? 'tw-bg-[var(--app-accent-brass)] tw-text-white tw-shadow-sm'
              : 'tw-bg-[var(--app-surface-container)] tw-text-[var(--app-on-surface-variant)] group-hover:tw-text-[var(--app-on-surface)]'
          ]"
        >
          <span class="material-symbols-outlined notranslate tw-text-base">
            {{ tab.icon }}
          </span>
        </div>

        <span class="tw-whitespace-nowrap">{{ tab.label }}</span>

        <!-- Línea sutil de acento inferior en tono latón/naranja para reforzar la pestaña activa -->
        <span
          v-if="isActive(tab.routeName)"
          class="tw-absolute tw-bottom-0 tw-left-0 tw-right-0 tw-h-[3px] tw-bg-[var(--app-accent-brass)] tw-rounded-t-full"
        />
      </button>
    </nav>
  </div>
</template>