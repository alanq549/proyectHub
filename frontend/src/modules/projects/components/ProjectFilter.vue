<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  categories?: string[]
}>()

const emit = defineEmits<{
  (e: 'filterChange', filters: { search: string; category: string }): void
}>()

const search = ref('')
const selectedCategory = ref('')

let timeout: ReturnType<typeof setTimeout>

watch([search, selectedCategory], () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    emit('filterChange', {
      search: search.value.trim(),
      category: selectedCategory.value
    })
  }, 300)
})
</script>

<template>
  <div class="project-filter">
    <div class="search-box">
      <input
        v-model="search"
        type="text"
        placeholder="Buscar proyectos..."
        class="filter-input"
      />
    </div>

    <div v-if="categories && categories.length" class="category-box">
      <select v-model="selectedCategory" class="filter-select">
        <option value="">Todas las categorías</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
    </div>
  </div>
</template>

<style scoped>
.project-filter {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-input,
.filter-select {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  color: inherit;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.filter-input:focus,
.filter-select:focus {
  border-color: #42b883;
}

.search-box {
  flex: 1;
  min-width: 200px;
}

.filter-input {
  width: 100%;
}
</style>