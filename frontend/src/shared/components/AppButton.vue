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

const baseClasses = 'inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-slate-900/20 active:scale-[0.98] disabled:opacity-60 disabled:pointer-events-none cursor-pointer'

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-slate-900 hover:bg-black text-white shadow-btn-primary hover:shadow-btn-primary-hover border border-slate-800'
    case 'secondary':
      return 'bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-200/80 shadow-sm'
    case 'outline':
      return 'bg-transparent hover:bg-slate-100/80 text-slate-700 border border-slate-300 hover:border-slate-400'
    case 'ghost':
      return 'bg-transparent hover:bg-slate-100 text-slate-600 hover:text-slate-900'
    case 'danger':
      return 'bg-error hover:bg-red-700 text-white shadow-sm border border-red-700'
    default:
      return ''
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-3 py-1.5 text-xs gap-1.5'
    case 'lg':
      return 'px-6 py-3 text-base gap-2.5'
    case 'md':
    default:
      return 'px-4 py-2 text-sm gap-2'
  }
})

const widthClass = computed(() => (props.block ? 'w-full' : ''))

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
    <span v-if="loading" class="animate-spin inline-block w-4 h-4 border-2 border-current border-t-transparent rounded-full" aria-hidden="true"></span>
    <span v-else-if="icon" class="material-symbols-outlined text-[1.2em] notranslate" aria-hidden="true">{{ icon }}</span>
    <slot name="icon" v-else-if="$slots.icon"></slot>
    <slot></slot>
  </button>
</template>
