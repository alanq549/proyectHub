<template>
  <div ref="dropdownRef" class="relative inline-block">
    <slot
      name="trigger"
      :open="isOpen"
      :toggle="toggle"
    >
      <button
        type="button"
        class="inline-flex items-center justify-center p-2 rounded-xl outline-none"
        :aria-expanded="isOpen"
        aria-haspopup="true"
        role="button"
        @click="toggle"
      >
        <span class="material-symbols-outlined notranslate">more_vert</span>
      </button>
    </slot>

    <Teleport to="body">
      <Transition name="dropdown-fade">
        <div
          v-if="isOpen && floatingStyles"
          class="z-[1060]"
          :style="floatingStyles"
          role="menu"
        >
          <div
            class="bg-white backdrop-blur-glass-sm rounded-2xl border border-slate-100 shadow-lg py-2 min-w-[220px]"
            @click.stop
          >
            <slot :close="close" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, nextTick } from 'vue';
import { useClickOutside } from '../composables/useClickOutside';

const props = defineProps<{
  modelValue?: boolean;
  align?: 'start' | 'end';
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', v: boolean): void;
  (e: 'open'): void;
  (e: 'close'): void;
}>();

const dropdownRef = ref<HTMLElement | null>(null);
const isOpen = ref(props.modelValue ?? false);
const top = ref(0);
const left = ref(0);

watch(
  () => props.modelValue,
  (v) => {
    isOpen.value = v ?? false;
  },
);

const floatingStyles = computed(() => {
  if (!isOpen.value) return null;
  return {
    position: 'absolute' as const,
    top: `${top.value}px`,
    left: `${left.value}px`,
  };
});

function close() {
  isOpen.value = false;
  emit('update:modelValue', false);
  emit('close');
}

function open() {
  isOpen.value = true;
  emit('update:modelValue', true);
  emit('open');
}

function toggle() {
  if (isOpen.value) {
    close();
  } else {
    open();
  }
}

function computePosition() {
  const root = dropdownRef.value;
  if (!root) return;
  const rect = root.getBoundingClientRect();
  const align = props.align ?? 'end';
  top.value = window.scrollY + rect.bottom + 6;
  if (align === 'end') {
    const menuWidth = 220;
    left.value = window.scrollX + rect.right - menuWidth;
  } else {
    left.value = window.scrollX + rect.left;
  }
}

watch(isOpen, async (openNow) => {
  if (openNow) {
    await nextTick();
    computePosition();
  }
});

window.addEventListener('resize', () => {
  if (isOpen.value) computePosition();
});
window.addEventListener('scroll', () => {
  if (isOpen.value) computePosition();
}, true);

useClickOutside(dropdownRef, () => {
  if (isOpen.value) close();
});

defineExpose({ open, close, toggle });
</script>

<style>
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: opacity 0.12s ease, transform 0.12s ease;
}
.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
