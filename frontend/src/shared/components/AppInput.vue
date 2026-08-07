<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue?: string | number
  type?: 'text' | 'password' | 'email' | 'number' | 'tel'
  placeholder?: string
  disabled?: boolean
  error?: string
  icon?: string
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: '',
  type: 'text',
  placeholder: '',
  disabled: false,
  error: '',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
}>()

const baseClasses = 'tw-w-full tw-rounded-xl tw-border tw-border-outline-variant tw-bg-surface-container-lowest tw-px-4 tw-py-2.5 tw-text-sm tw-text-on-surface tw-transition-colors tw-duration-200 focus:tw-border-primary focus:tw-outline-none focus:tw-ring-1 focus:tw-ring-primary disabled:tw-cursor-not-allowed disabled:tw-bg-surface-container-low disabled:tw-text-on-surface-variant'

const errorClasses = computed(() => {
  return props.error ? 'tw-border-error focus:tw-border-error focus:tw-ring-error' : ''
})

const paddingClasses = computed(() => {
  return props.icon ? 'tw-pl-10' : ''
})

function onInput(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="tw-w-full">
    <div class="tw-relative">
      <span v-if="icon" class="material-symbols-outlined tw-absolute tw-left-3 tw-top-1/2 -tw-translate-y-1/2 tw-text-[1.2rem] tw-text-outline notranslate" aria-hidden="true">{{ icon }}</span>
      <input
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :class="[baseClasses, errorClasses, paddingClasses]"
        @input="onInput"
      />
    </div>
    <p v-if="error" class="tw-mt-1.5 tw-text-xs tw-text-error tw-font-medium">{{ error }}</p>
  </div>
</template>
