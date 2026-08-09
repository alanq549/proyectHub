<script setup lang="ts">
import type { Project } from '../services/projectService'

defineProps<{
  project: Project
}>()

const emit = defineEmits<{
  (e: 'click', id: number): void
}>()
</script>

<template>
  <div class="project-card" @click="emit('click', project.id)">
    <div class="card-header">
      <h3 class="card-title">{{ project.title }}</h3>
      <span v-if="project.category" class="badge">{{ project.category }}</span>
    </div>
    
    <p class="card-description">{{ project.description }}</p>
    
    <div class="card-footer">
      <span v-if="project.status" class="status-tag" :class="project.status.toLowerCase()">
        {{ project.status }}
      </span>
      <span class="action-text">Ver detalles &rarr;</span>
    </div>
  </div>
</template>

<style scoped>
.project-card {
  padding: 1.25rem;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.project-card:hover {
  transform: translateY(-3px);
  border-color: rgba(66, 184, 131, 0.4);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.card-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 600;
}

.badge {
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  background: rgba(66, 184, 131, 0.15);
  color: #42b883;
}

.card-description {
  font-size: 0.9rem;
  opacity: 0.8;
  line-height: 1.4;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.action-text {
  color: #42b883;
  font-weight: 500;
}
</style>