<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { projectService, type Project } from '../services/projectService'
import ProjectCard from '../components/ProjectCard.vue'
import ProjectFilter from '../components/ProjectFilter.vue'

const router = useRouter()
const projects = ref<Project[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const fetchProjects = async (filters?: { search?: string; category?: string }) => {
  loading.value = true
  error.value = null
  try {
    projects.value = await projectService.getAll(filters)
  } catch (err: any) {
    error.value = err?.response?.data?.message || 'Error al cargar los proyectos.'
  } finally {
    loading.value = false
  }
}

const handleFilterChange = (filters: { search: string; category: string }) => {
  fetchProjects(filters)
}

const goToDetail = (id: number) => {
  router.push({ name: 'project-detail', params: { id } })
}

onMounted(() => {
  fetchProjects()
})
</script>

<template>
  <div class="projects-list-container">
    <header class="header">
      <h1>Proyectos</h1>
    </header>

    <ProjectFilter @filter-change="handleFilterChange" />

    <div v-if="loading" class="state-message">Cargando proyectos...</div>

    <div v-else-if="error" class="state-message error">{{ error }}</div>

    <div v-else-if="projects.length === 0" class="state-message">
      No se encontraron proyectos.
    </div>

    <div v-else class="projects-grid">
      <ProjectCard
        v-for="project in projects"
        :key="project.id"
        :project="project"
        @click="goToDetail"
      />
    </div>
  </div>
</template>

<style scoped>
.projects-list-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 2rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.state-message {
  text-align: center;
  padding: 3rem;
  opacity: 0.7;
}

.state-message.error {
  color: #ff5252;
  opacity: 1;
}
</style>