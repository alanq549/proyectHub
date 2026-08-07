<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  loading?: boolean
  icon?: string
  block?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  type: 'button',
  disabled: false,
  loading: false,
  block: false,
})

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const baseClasses = 'tw-inline-flex tw-items-center tw-justify-center tw-font-medium tw-rounded-xl tw-transition-all tw-duration-200 focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-primary/20 active:tw-scale-[0.98] disabled:tw-opacity-60 disabled:tw-pointer-events-none tw-cursor-pointer'

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'tw-bg-primary hover:tw-bg-primary-dark tw-text-on-primary tw-shadow-btn-primary hover:tw-shadow-btn-primary-hover tw-border tw-border-primary-dark'
    case 'secondary':
      return 'tw-bg-surface-container-low hover:tw-bg-surface-container tw-text-on-surface tw-border tw-border-outline-variant tw-shadow-sm'
    case 'outline':
      return 'tw-bg-transparent hover:tw-bg-surface-container-low tw-text-on-surface-variant tw-border tw-border-outline-variant hover:tw-border-outline'
    case 'ghost':
      return 'tw-bg-transparent hover:tw-bg-surface-container-low tw-text-on-surface-variant hover:tw-text-on-surface'
    case 'danger':
      return 'tw-bg-error hover:tw-bg-error/90 tw-text-on-primary tw-shadow-sm tw-border tw-border-error'
    default:
      return ''
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'tw-px-3 tw-py-1.5 tw-text-xs tw-gap-1.5'
    case 'lg':
      return 'tw-px-6 tw-py-3 tw-text-base tw-gap-2.5'
    case 'md':
    default:
      return 'tw-px-4 tw-py-2 tw-text-sm tw-gap-2'
  }
})

const widthClass = computed(() => (props.block ? 'tw-w-full' : ''))

function handleClick(event: MouseEvent) {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[baseClasses, variantClasses, sizeClasses, widthClass]"
    @click="handleClick"
  >
    <span v-if="loading" class="tw-animate-spin tw-inline-block tw-w-4 tw-h-4 tw-border-2 tw-border-current tw-border-t-transparent tw-rounded-full" aria-hidden="true"></span>
    <span v-else-if="icon" class="material-symbols-outlined tw-text-[1.2em] notranslate" aria-hidden="true">{{ icon }}</span>
    <slot name="icon" v-else-if="$slots.icon"></slot>
    <slot></slot>
  </button>
</template>
