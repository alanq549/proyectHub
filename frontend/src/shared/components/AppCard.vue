<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'glass' | 'glass-xl' | 'glass-light' | 'flat' | 'outlined'
  padding?: 'none' | 'sm' | 'md' | 'lg'
  hoverable?: boolean
  color?: string // Opcional por si quieres pasar un color/gradiente personalizado
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'glass',
  padding: 'md',
  hoverable: false,
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'glass':
      // Blanco translúcido (80% opacidad) con borde superior/lateral brillante y sombra glass
      return 'tw-bg-white/80 tw-backdrop-blur-glass tw-border tw-border-white/90 tw-border-b-black/5 tw-shadow-glass tw-rounded-glass-md'
    case 'glass-xl':
      return 'tw-bg-white/75 tw-backdrop-blur-glass tw-border tw-border-white/90 tw-border-b-primary/10 tw-shadow-glass tw-rounded-glass-xl'
    case 'glass-light':
      return 'tw-bg-white/50 tw-backdrop-blur-glass-sm tw-border tw-border-white/60 tw-shadow-sm tw-rounded-glass-sm'
    case 'flat':
      return 'tw-bg-white tw-border tw-border-slate-200 tw-shadow-card-flat tw-rounded-2xl'
    case 'outlined':
      return 'tw-bg-transparent tw-border tw-border-slate-200 tw-rounded-2xl'
    default:
      return 'tw-bg-white/80 tw-backdrop-blur-glass tw-border tw-border-white/90 tw-shadow-glass tw-rounded-glass-md'
  }
})

const hoverClasses = computed(() => {
  if (!props.hoverable) return ''
  switch (props.variant) {
    case 'glass':
    case 'glass-xl':
      return 'tw-transition-all tw-duration-250 tw-ease-out hover:tw-bg-white/95 hover:tw-shadow-glass-hover hover:-tw-translate-y-0.5'
    case 'glass-light':
      return 'tw-transition-all tw-duration-200 tw-ease-out hover:tw-shadow-md hover:-tw-translate-y-0.5'
    case 'flat':
    case 'outlined':
      return 'tw-transition-all tw-duration-200 tw-ease-out hover:tw-border-slate-400 hover:tw-shadow-md'
    default:
      return 'tw-transition-all tw-duration-250 tw-ease-out hover:tw-shadow-glass-hover'
  }
})

const paddingClasses = computed(() => {
  switch (props.padding) {
    case 'none':
      return 'tw-p-0'
    case 'sm':
      return 'tw-p-4'
    case 'lg':
      return 'tw-p-6 sm:tw-p-8'
    case 'md':
    default:
      return 'tw-p-5 sm:tw-p-6'
  }
})
</script>

<template>
  <div 
    :class="[variantClasses, hoverClasses, paddingClasses, props.color, 'tw-relative tw-overflow-hidden']"
  >
    <div 
      v-if="$slots.header"
      class="tw-mb-4 tw-pb-3 tw-border-b tw-border-slate-200/60 tw-flex tw-items-center tw-justify-between"
    >
      <slot name="header"></slot>
    </div>

    <slot></slot>

    <div 
      v-if="$slots.footer"
      class="tw-mt-4 tw-pt-3 tw-border-t tw-border-slate-200/60 tw-flex tw-items-center tw-justify-between"
    >
      <slot name="footer"></slot>
    </div>
  </div>
</template>