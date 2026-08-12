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

// Helper para leer el mensaje de error de una respuesta Axios sin usar 'any'
function extractErrorMessage(err: unknown, fallback: string): string {
  const axiosErr = err as { response?: { data?: { message?: string } } }
  return axiosErr?.response?.data?.message || fallback
}

const fetchProjects = async (filters?: { search?: string; category?: string }) => {
  loading.value = true
  error.value = null
  try {
    projects.value = await projectService.getAll(filters)
  } catch (err: unknown) {
    error.value = extractErrorMessage(err, 'Error al cargar los proyectos.')
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
      <p class="header-subtitle">Consulta y da seguimiento a los proyectos registrados.</p>
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
/* ============================================================
   Paleta "PROJECTHUB" — navy #10192B + dorado #C9974A
   Coherente con Login, Register, CallCard y el dashboard.
   ============================================================ */

.projects-list-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  background-color: var(--background, #f7f9fb);
}

.header {
  margin-bottom: 2rem;
}

.header h1 {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-weight: 700;
  color: var(--ph-navy, #10192B);
  margin: 0 0 0.35rem;
}

.header-subtitle {
  color: var(--on-surface-variant, #45464d);
  font-size: 0.95rem;
  margin: 0;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.state-message {
  text-align: center;
  padding: 3rem;
  color: var(--on-surface-variant, #45464d);
}

.state-message.error {
  color: var(--app-error, #ba1a1a);
}
</style>
