<template>
  <div class="af-dashboard">
    <DashboardHeroCard
      :user="heroUser"
      @download-report="$emit('download-report')"
      @new-audit="$emit('new-audit')"
    />

    <DashboardKpiGrid :kpis="kpis" />

    <div class="row g-4">
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

      <div class="col-12 col-lg-4 d-flex flex-column gap-4">
        <DashboardS3UploadPanel @browse="$emit('upload-file')" />

        <DashboardSystemHealthPanel
          :metrics="systemMetrics"
          :buckets-active="bucketsActive"
          :total-buckets="totalBuckets"
        />

        <DashboardSupportCard @contact="$emit('contact-support')" />
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
import DashboardSupportCard from '../components/DashboardSupportCard.vue'

const VITE_STATIC_URL = import.meta.env.VITE_STATIC_URL
const authStore = useAuthStore()

const DEFAULT_AVATAR = `${VITE_STATIC_URL}/static/defaults/icon_default.png`

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

// -- KPIs --
const kpis: Kpi[] = [
  {
    label: 'Usuarios Registrados',
    value: '128',
    icon: 'group',
    iconBg: 'rgba(75,65,225,0.10)',
    iconColor: '#4b41e1',
    trend: '+12%',
  },
  {
    label: 'Convocatorias Activas',
    value: '8',
    icon: 'campaign',
    iconBg: 'rgba(76,215,246,0.10)',
    iconColor: '#0090a9',
    tag: 'En Curso',
  },
  {
    label: 'Proyectos Totales',
    value: '45',
    icon: 'folder_open',
    iconBg: '#dbeafe',
    iconColor: '#1d4ed8',
    breakdown: { positive: '30 Aprobados', neutral: '15 Revisión' },
  },
  {
    label: 'S3 Storage',
    value: '1.2',
    unit: 'TB',
    icon: 'cloud_upload',
    iconBg: '#ffedd5',
    iconColor: '#c2410c',
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
    iconBg: '#131b2e',
  },
  {
    name: 'Red de Sensores IoT',
    date: '08 Oct 2023',
    status: 'En Revisión',
    icon: 'sensors',
    iconBg: '#001f26',
  },
  {
    name: 'IA Educativa Pro',
    date: '05 Oct 2023',
    status: 'Aprobado',
    icon: 'psychology',
    iconBg: '#645efb',
  },
]

// -- Convocatorias vigentes --
const activeCalls: ActiveCall[] = [
  {
    title: 'Beca I+D 2024',
    org: 'FONCYT',
    orgBg: '#dbeafe',
    orgColor: '#1e40af',
    description: 'Apoyo a proyectos de biotecnología avanzada y sostenibilidad climática.',
    deadline: '30 Noviembre',
  },
  {
    title: 'Innova Académica',
    org: 'MINCYT',
    orgBg: '#f3e8ff',
    orgColor: '#6b21a8',
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

// -- Emits --
defineEmits<{
  (event: 'download-report'): void
  (event: 'new-audit'): void
  (event: 'view-all-projects'): void
  (event: 'view-project', project: RecentProject): void
  (event: 'apply-call', call: ActiveCall): void
  (event: 'upload-file'): void
  (event: 'contact-support'): void
}>()
</script>

<style scoped>
.af-dashboard {
  --af-primary: #000000;
  --af-primary-container: #131b2e;
  --af-secondary: #4b41e1;
  --af-secondary-container: #645efb;
  --af-on-secondary-container: #fffbff;
  --af-tertiary-fixed-dim: #4cd7f6;
  --af-on-tertiary-container: #0090a9;
  --af-tertiary-fixed: #acedff;
  --af-on-tertiary-fixed-variant: #004e5c;
  --af-surface: #f7f9fb;
  --af-surface-container: #eceef0;
  --af-surface-container-low: #f2f4f6;
  --af-surface-container-highest: #e0e3e5;
  --af-outline-variant: #c6c6cd;
  --af-on-surface: #191c1e;
  --af-on-surface-variant: #45464d;
  --af-error: #ba1a1a;

  font-family: 'Inter', sans-serif;
  color: var(--af-on-surface);
}
</style>
