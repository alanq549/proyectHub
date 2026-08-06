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

const baseClasses = 'inline-flex items-center font-semibold rounded-full transition-colors'

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'success':
      return 'bg-emerald-50 text-emerald-700 border border-emerald-200/60'
    case 'warning':
      return 'bg-amber-50 text-amber-700 border border-amber-200/60'
    case 'error':
      return 'bg-rose-50 text-rose-700 border border-rose-200/60'
    case 'info':
      return 'bg-sky-50 text-sky-700 border border-sky-200/60'
    case 'primary':
      return 'bg-slate-900 text-white border border-slate-800'
    case 'neutral':
    default:
      return 'bg-slate-100 text-slate-700 border border-slate-200'
  }
})

const dotColorClass = computed(() => {
  switch (props.variant) {
    case 'success':
      return 'bg-emerald-500'
    case 'warning':
      return 'bg-amber-500'
    case 'error':
      return 'bg-rose-500'
    case 'info':
      return 'bg-sky-500'
    case 'primary':
      return 'bg-white'
    case 'neutral':
    default:
      return 'bg-slate-400'
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2 py-0.5 text-[11px] gap-1'
    case 'md':
    default:
      return 'px-2.5 py-1 text-xs gap-1.5'
  }
})
</script>

<template>
  <span :class="[baseClasses, variantClasses, sizeClasses]">
    <span v-if="dot" :class="['inline-block w-1.5 h-1.5 rounded-full', dotColorClass]" aria-hidden="true"></span>
    <span v-else-if="icon" class="material-symbols-outlined text-[1.1em] notranslate" aria-hidden="true">{{ icon }}</span>
    <slot></slot>
  </span>
</template>
