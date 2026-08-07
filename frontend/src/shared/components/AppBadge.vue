<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'success' | 'warning' | 'error' | 'info' | 'primary' | 'neutral'
  size?: 'sm' | 'md'
  dot?: boolean
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'neutral',
  size: 'md',
  dot: false,
})

const baseClasses = 'tw-inline-flex tw-items-center tw-font-semibold tw-rounded-full tw-transition-colors'

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'success':
      return 'tw-bg-success-bg tw-text-success tw-border tw-border-success/30'
    case 'warning':
      return 'tw-bg-warning-bg tw-text-warning tw-border tw-border-warning/30'
    case 'error':
      return 'tw-bg-error-bg tw-text-error tw-border tw-border-error/30'
    case 'info':
      return 'tw-bg-surface-container-low tw-text-on-surface-variant tw-border tw-border-outline-variant'
    case 'primary':
      return 'tw-bg-primary tw-text-on-primary tw-border tw-border-primary-dark'
    case 'neutral':
    default:
      return 'tw-bg-surface-container tw-text-on-surface tw-border tw-border-outline-variant'
  }
})

const dotColorClass = computed(() => {
  switch (props.variant) {
    case 'success':
      return 'tw-bg-success'
    case 'warning':
      return 'tw-bg-warning'
    case 'error':
      return 'tw-bg-error'
    case 'info':
      return 'tw-bg-on-surface-variant'
    case 'primary':
      return 'tw-bg-on-primary'
    case 'neutral':
    default:
      return 'tw-bg-outline'
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'tw-px-2 tw-py-0.5 tw-text-[11px] tw-gap-1'
    case 'md':
    default:
      return 'tw-px-2.5 tw-py-1 tw-text-xs tw-gap-1.5'
  }
})
</script>

<template>
  <span :class="[baseClasses, variantClasses, sizeClasses]">
    <span v-if="dot" :class="['tw-inline-block tw-w-1.5 tw-h-1.5 tw-rounded-full', dotColorClass]" aria-hidden="true"></span>
    <span v-else-if="icon" class="material-symbols-outlined tw-text-[1.1em] notranslate" aria-hidden="true">{{ icon }}</span>
    <slot></slot>
  </span>
</template>
