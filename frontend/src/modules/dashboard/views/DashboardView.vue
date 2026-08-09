<template>
  <!--
    DashboardView — Bloque 1.1 (Migración Bootstrap → Tailwind)
    • Todas las utilidades layout (d-flex, row, col-*, gap-*) migradas.
    • Tokens via theme.extend: colors/shadow/blur/radius siguen pasando por --app-*.
    • Bootstrap sigue cargado globalmente = convivencia sin conflictos (prefijo ).
  -->
  <div class="af-dashboard tw-flex tw-flex-col tw-gap-4">
    <!-- 1. Hero Card -->
    <DashboardHeroCard
      :user="heroUser"
      :primary-action-label="isAdmin ? 'Gestionar usuarios' : 'Ver convocatorias'"
      :secondary-action-label="isAdmin ? 'Gestionar convocatorias' : 'Mis proyectos'"
      @primary-action="goToPrimaryAction"
      @secondary-action="goToSecondaryAction"
    />

    <!-- 2. Grid de 4 KPIs -->
    <DashboardKpiGrid :kpis="kpis" />

    <!-- 3. Contenido Principal en 2 Columnas (mobile 1 / desktop 8+4 = 12 cols) -->
    <div class="tw-grid tw-grid-cols-1 lg:tw-grid-cols-12 tw-gap-4">
      <!-- Columna Izquierda (Proyectos Recientes + Convocatorias) -->
      <div class="lg:tw-col-span-12 tw-flex tw-flex-col tw-gap-4">
        <DashboardRecentProjects
          :projects="recentProjects"
          :loading="loading"
          :title="isAdmin ? 'Proyectos recientes globales' : 'Mis proyectos recientes'"
          @view-all="router.push({ name: 'projects-list' })"
          @view-project="goToProject"
        />

        <DashboardActiveCalls
          :calls="activeCalls"
          :loading="loading"
          :action-label="isAdmin ? 'Gestionar' : 'Ver convocatoria'"
          @apply="goToCall"
        />
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { callService, type Call } from '@/modules/calls/services/callService'
import { projectService, type Project } from '@/modules/projects/services/projectService'
import { documentService, type DocumentModel } from '@/modules/documents/services/documentService'
import { userService, type User as ManagedUser } from '@/modules/user/services/userService'
import DashboardHeroCard, { type DashboardHeroUser } from '../components/DashboardHeroCard.vue'
import DashboardKpiGrid, { type Kpi } from '../components/DashboardKpiGrid.vue'
import DashboardRecentProjects, { type RecentProject } from '../components/DashboardRecentProjects.vue'
import DashboardActiveCalls, { type ActiveCall } from '../components/DashboardActiveCalls.vue'

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(true)
const calls = ref<Call[]>([])
const projects = ref<Project[]>([])
const documents = ref<DocumentModel[]>([])
const users = ref<ManagedUser[]>([])
const isAdmin = computed(() => authStore.isAdmin)

const ROLE_LABELS: Record<'admin' | 'user', string> = {
  admin: 'Administrador del Sistema',
  user: 'Usuario',
}

function buildDisplayName(): string {
  const u = authStore.user
  if (!u) return 'Usuario'
  const parts: string[] = []
  if (u.first_name) parts.push(u.first_name)
  if (u.last_name) parts.push(u.last_name)
  if (parts.length > 0) return parts.join(' ')
  return u.username
}

function buildRoleLabel(): string {
  const u = authStore.user
  if (!u) return 'Usuario'
  return ROLE_LABELS[u.role] ?? u.role
}

const heroUser = computed<DashboardHeroUser>(() => ({
  name: buildDisplayName(),
  role: buildRoleLabel(),
  avatarUrl: authStore.avatarUrl,
}))

// -- KPIs en Paleta Blanco / Negro / Slate --
const mockKpis: Kpi[] = [
  {
    label: 'Usuarios Registrados',
    value: '128',
    icon: 'group',
    iconBg: 'rgba(15, 23, 42, 0.06)',
    iconColor: '#0f172a',
    trend: '+12%',
  },
  {
    label: 'Convocatorias Activas',
    value: '8',
    icon: 'campaign',
    iconBg: 'rgba(15, 23, 42, 0.06)',
    iconColor: '#0f172a',
    tag: 'En Curso',
  },
  {
    label: 'Proyectos Totales',
    value: '45',
    icon: 'folder_open',
    iconBg: 'rgba(15, 23, 42, 0.06)',
    iconColor: '#0f172a',
    breakdown: { positive: '30 Aprobados', neutral: '15 Revisión' },
  },
  {
    label: 'Almacenamiento S3',
    value: '1.2',
    unit: 'TB',
    icon: 'cloud_upload',
    iconBg: 'rgba(15, 23, 42, 0.06)',
    iconColor: '#0f172a',
    footnote: '85% Capacidad',
  },
]

// -- Proyectos recientes --
const mockRecentProjects: RecentProject[] = [
  {
    name: 'Análisis Genómico',
    date: '12 Oct 2023',
    status: 'Aprobado',
    icon: 'strikethrough_s',
    iconBg: '#FDFDFE',
  },
  {
    name: 'Red de Sensores IoT',
    date: '08 Oct 2023',
    status: 'En Revisión',
    icon: 'sensors',
    iconBg: '##FDFDFE',
  },
  {
    name: 'IA Educativa Pro',
    date: '05 Oct 2023',
    status: 'Aprobado',
    icon: 'psychology',
    iconBg: '##FDFDFE',
  },
]

// -- Convocatorias vigentes --
const mockActiveCalls: ActiveCall[] = [
  {
    title: 'FONCYT 1',
    org: 'Cierra en 3 días',
    orgBg: '#fef2f2',
    orgColor: '#b91c1c',
    description: 'Apoyo a proyectos de biotecnología avanzada y sostenibilidad climática.',
    deadline: '30 Noviembre',
  },
  {
    title: 'FONCYT 2',
    org: 'Cierra en 3 días',
    orgBg: '#fef2f2',
    orgColor: '#b91c1c',
    description: 'Fondos para la modernización de infraestructuras de investigación digital.',
    deadline: '15 Diciembre',
  },
]

// -- Estado del sistema --
const systemMetrics: Array<{ label: string; value: string; percent: number }> = [
  { label: 'API Latency', value: '24ms', percent: 15 },
  { label: 'DB Performance', value: '98.4%', percent: 98 },
]
const totalBuckets = 5
const bucketsActive = 4

const activeCallsSource = computed(() => calls.value.filter((call) => {
  const deadline = new Date(call.end_date)
  return call.is_active && !Number.isNaN(deadline.getTime()) && deadline >= new Date()
}))

const kpis = computed<Kpi[]>(() => {
  const approved = projects.value.filter((project) => project.status === 'approved').length
  const inReview = projects.value.filter((project) => ['submitted', 'in_review'].includes(project.status || '')).length
  const makeKpi = (label: string, value: number, icon: string, footnote: string): Kpi => ({
    label, value: String(value), icon, footnote,
    iconBg: 'rgba(15, 23, 42, 0.06)', iconColor: '#0f172a',
  })

  if (isAdmin.value) {
    const applications = calls.value.reduce((total, call) => total + Number((call as Call & { participants_count?: number }).participants_count ?? 0), 0)
    return [
      makeKpi('Usuarios registrados', users.value.length, 'group', `${users.value.filter((user) => user.is_active !== false).length} activos`),
      makeKpi('Convocatorias vigentes', activeCallsSource.value.length, 'campaign', `${calls.value.length} en total`),
      makeKpi('Proyectos totales', projects.value.length, 'folder_open', `${approved} aprobados · ${inReview} en revisión`),
      makeKpi('Postulaciones recibidas', applications, 'assignment', 'En todas las convocatorias'),
    ]
  }

  return [
    makeKpi('Mis proyectos', projects.value.length, 'folder_open', `${approved} aprobados`),
    makeKpi('Convocatorias vigentes', activeCallsSource.value.length, 'campaign', 'Disponibles para postular'),
    makeKpi('Proyectos en revisión', inReview, 'pending_actions', 'Enviados o en revisión'),
    makeKpi('Mis documentos', documents.value.length, 'description', 'Archivos cargados'),
  ]
})

const recentProjects = computed<RecentProject[]>(() => projects.value
  .slice()
  .sort((a, b) => Date.parse(b.updated_at || b.created_at || '') - Date.parse(a.updated_at || a.created_at || ''))
  .slice(0, 5)
  .map((project) => ({
    id: project.id,
    name: project.title,
    subtitle: project.call_title || project.description,
    team: isAdmin.value ? (project.call_title || 'Proyecto independiente') : 'Mi proyecto',
    date: formatDate(project.updated_at || project.created_at),
    status: projectStatusLabel(project.status),
    icon: 'folder',
  })))

const activeCalls = computed<ActiveCall[]>(() => activeCallsSource.value
  .slice()
  .sort((a, b) => Date.parse(a.end_date) - Date.parse(b.end_date))
  .slice(0, 4)
  .map((call) => ({
    id: call.id,
    title: call.title,
    org: `Cierra ${formatDate(call.end_date)}`,
    orgBg: '#fef2f2',
    orgColor: '#b91c1c',
    description: call.description || 'Sin descripción disponible.',
    deadline: formatDate(call.end_date),
  })))

function formatDate(value?: string) {
  if (!value) return 'Sin fecha'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? 'Sin fecha' : new Intl.DateTimeFormat('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }).format(date)
}

function projectStatusLabel(status?: string) {
  const labels: Record<string, string> = { draft: 'Borrador', submitted: 'Enviado', in_review: 'En revisión', approved: 'Aprobado', rejected: 'Rechazado' }
  return labels[status || ''] || status || 'Sin estado'
}

async function loadDashboard() {
  loading.value = true
  try {
    const [loadedCalls, loadedProjects, loadedDocuments, loadedUsers] = await Promise.all([
      callService.getCalls(),
      projectService.getAll(),
      documentService.getDocuments(),
      isAdmin.value ? userService.getUsers() : Promise.resolve([] as ManagedUser[]),
    ])
    calls.value = loadedCalls
    projects.value = loadedProjects
    documents.value = loadedDocuments
    users.value = loadedUsers
  } catch (error) {
    console.error('Error cargando el dashboard:', error)
  } finally {
    loading.value = false
  }
}

function goToPrimaryAction() {
  router.push({ name: isAdmin.value ? 'users-list' : 'calls-list' })
}

function goToSecondaryAction() {
  router.push({ name: isAdmin.value ? 'calls-list' : 'projects-list' })
}

function goToProject(project: RecentProject) {
  if (project.id) router.push({ name: 'project-detail', params: { id: project.id } })
}

function goToCall(call: ActiveCall) {
  if (isAdmin.value) {
    router.push({ name: 'calls-list' })
  } else if (call.id) {
    router.push({ name: 'call-detail', params: { id: call.id } })
  }
}

onMounted(loadDashboard)

defineEmits<{
  (event: 'download-report'): void
  (event: 'new-audit'): void
  (event: 'manage-users'): void
  (event: 'view-all-projects'): void
  (event: 'view-project', project: RecentProject): void
  (event: 'apply-call', call: ActiveCall): void
  (event: 'upload-file'): void
  (event: 'contact-support'): void
}>()
</script>

<style scoped>
.af-dashboard {
  font-family: var(--app-font-family, 'Inter', sans-serif);
}
</style>
