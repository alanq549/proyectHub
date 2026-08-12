<template>
  <div v-if="errorMessage" class="error-alert">
    <span class="material-symbols-outlined notranslate">
      error
    </span>

    <p>
      {{ errorMessage }}
    </p>
  </div>
</template>

<script setup lang="ts">

defineProps<{
  errorMessage: string;
}>();

</script>

<style scoped>
.error-alert {
  /* display: none; */
  /* Handled by Vue's :style binding */
  margin-bottom: 24px;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: rgba(242, 109, 120, 0.12);
  border: 1px solid rgba(242, 109, 120, 0.25);
  align-items: center;
  gap: 0.75rem;
}

.error-alert .material-symbols-outlined {
  color: var(--error, #F26D78);
}

.error-alert p {
  color: var(--on-error-container, #9A2530);
  font-size: 14px;
  margin: 0;
}
</style>
