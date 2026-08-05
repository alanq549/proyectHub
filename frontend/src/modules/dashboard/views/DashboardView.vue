<template>
  <div class="af-dashboard d-flex flex-column gap-4">
    <!-- 1. Hero Card -->
    <DashboardHeroCard
      :user="heroUser"
      @download-report="$emit('download-report')"
      @new-audit="$emit('new-audit')"
      @manage-users="$emit('manage-users')"
    />

    <!-- 2. Grid de 4 KPIs -->
    <DashboardKpiGrid :kpis="kpis" />

    <!-- 3. Contenido Principal en 2 Columnas -->
    <div class="row g-4">
      <!-- Columna Izquierda (Proyectos Recientes + Convocatorias) -->
      <div class="col-12 col-lg-8 d-flex flex-column gap-4">
        <DashboardRecentProjects
          :projects="recentProjects"
          @view-all="$emit('view-all-projects')"
          @view-project="(p) => $emit('view-project', p)"
        />

        <DashboardActiveCalls
          :calls="activeCalls"
          @apply="(c) => $emit('apply-call', c)"
        />
      </div>

      <!-- Columna Derecha (Subir a S3 + Salud Detallada + Soporte) -->
      <div class="col-12 col-lg-4 d-flex flex-column gap-4">
        <DashboardS3UploadPanel @browse="$emit('upload-file')" />

        <DashboardSystemHealthPanel
          :metrics="systemMetrics"
          :buckets-active="bucketsActive"
          :total-buckets="totalBuckets"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import DashboardHeroCard, { type DashboardHeroUser } from '../components/DashboardHeroCard.vue'
import DashboardKpiGrid, { type Kpi } from '../components/DashboardKpiGrid.vue'
import DashboardRecentProjects, { type RecentProject } from '../components/DashboardRecentProjects.vue'
import DashboardActiveCalls, { type ActiveCall } from '../components/DashboardActiveCalls.vue'
import DashboardS3UploadPanel from '../components/DashboardS3UploadPanel.vue'
import DashboardSystemHealthPanel, { type SystemMetric } from '../components/DashboardSystemHealthPanel.vue'

const authStore = useAuthStore()

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
const kpis: Kpi[] = [
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
const recentProjects: RecentProject[] = [
  {
    name: 'Análisis Genómico',
    date: '12 Oct 2023',
    status: 'Aprobado',
    icon: 'strikethrough_s',
    iconBg: '#0f172a',
  },
  {
    name: 'Red de Sensores IoT',
    date: '08 Oct 2023',
    status: 'En Revisión',
    icon: 'sensors',
    iconBg: '#334155',
  },
  {
    name: 'IA Educativa Pro',
    date: '05 Oct 2023',
    status: 'Aprobado',
    icon: 'psychology',
    iconBg: '#0f172a',
  },
]

// -- Convocatorias vigentes --
const activeCalls: ActiveCall[] = [
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
const systemMetrics: SystemMetric[] = [
  { label: 'API Latency', value: '24ms', percent: 15 },
  { label: 'DB Performance', value: '98.4%', percent: 98 },
]
const totalBuckets = 5
const bucketsActive = 4

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