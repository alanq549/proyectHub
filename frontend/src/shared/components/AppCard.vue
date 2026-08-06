<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'glass' | 'glass-xl' | 'glass-light' | 'flat' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'glass',
  padding: 'md',
  hoverable: false,
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'glass':
      return 'bg-white/72 backdrop-blur-glass border border-white/90 border-b-black/5 shadow-glass rounded-glass-md'
    case 'glass-xl':
      return 'bg-white/72 backdrop-blur-glass border border-white/90 border-b-slate-900/10 shadow-glass rounded-glass-xl'
    case 'glass-light':
      return 'bg-white/55 backdrop-blur-glass-sm border border-white/50 shadow-sm rounded-glass-sm'
    case 'flat':
      return 'bg-white border border-slate-200 shadow-card-flat rounded-2xl'
    case 'outlined':
      return 'bg-transparent border border-slate-300 rounded-2xl'
    default:
      return 'bg-white/72 backdrop-blur-glass border border-white/90 shadow-glass rounded-glass-md'
  }
})

const hoverClasses = computed(() => {
  if (!props.hoverable) return ''
  switch (props.variant) {
    case 'glass':
    case 'glass-xl':
      return 'transition-all duration-250 ease-out hover:bg-white/88 hover:shadow-glass-hover hover:-translate-y-0.5'
    case 'glass-light':
      return 'transition-all duration-200 ease-out hover:shadow-md hover:-translate-y-0.5'
    case 'flat':
    case 'outlined':
      return 'transition-all duration-200 ease-out hover:border-slate-400 hover:shadow-md'
    default:
      return 'transition-all duration-250 ease-out hover:shadow-glass-hover'
  }
})

const paddingClasses = computed(() => {
  switch (props.padding) {
    case 'none':
      return 'p-0'
    case 'sm':
      return 'p-4'
    case 'lg':
      return 'p-6 sm:p-8'
    case 'md':
    default:
      return 'p-5 sm:p-6'
  }
})
</script>

<template>
  <div :class="[variantClasses, hoverClasses, paddingClasses, 'relative overflow-hidden']">
    <div v-if="$slots.header" class="mb-4 pb-3 border-b border-slate-100 flex items-center justify-between">
      <slot name="header"></slot>
    </div>
    <slot></slot>
    <div v-if="$slots.footer" class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
      <slot name="footer"></slot>
    </div>
  </div>
</template>
