<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { CallWorkspace } from '../services/workspaceService'
import { useAuthStore } from '@/stores/authStore' //[cite: 14]

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
      visible: isAdmin.value // Solo visible si es administrador
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
  <nav class="tw-flex tw-gap-1 tw-border-b tw-border-outline-variant tw-px-2 sm:tw-px-6">
    <button
      v-for="tab in tabs"
      :key="tab.name"
      type="button"
      @click="go(tab.routeName)"
      :class="[
        'tw-group tw-relative tw-flex tw-items-center tw-gap-2 tw-rounded-t-lg tw-px-4 tw-py-3 tw-text-sm tw-font-medium tw-transition-colors tw-duration-150',
        'focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-accent/20',
        isActive(tab.routeName)
          ? 'tw-bg-accent-bg tw-text-accent'
          : 'tw-text-on-surface-variant hover:tw-bg-surface-container-high hover:tw-text-on-surface'
      ]"
    >
      <span
        class="material-symbols-outlined notranslate tw-text-xl tw-transition-colors"
        :class="isActive(tab.routeName) ? 'tw-text-accent' : 'tw-text-on-surface-variant group-hover:tw-text-on-surface'"
      >
        {{ tab.icon }}
      </span>

      <span>{{ tab.label }}</span>

      <span
        v-if="isActive(tab.routeName)"
        class="tw-absolute tw-bottom-0 tw-left-0 tw-right-0 tw-h-0.5 tw-bg-accent"
      />
    </button>
  </nav>
</template>