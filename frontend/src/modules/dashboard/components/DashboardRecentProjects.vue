<template>
  <!--
    DashboardRecentProjects — Bloque 1.4 (Migración Bootstrap → Tailwind)
    • 35+ clases Bootstrap migradas (table-responsive, d-flex, gap-*, p-*, m-*,
      text-*, fw-bold, border-*, fs-*, d-none/d-md-block/d-md-none, etc.).
    • Glassmorphism mantiene clase global .app-card-glass-table (main.css).
    • Pills de estado usan clases semánticas af-status-pill.* intactas (estas
      usan tokens --app-success / --app-error / --app-warning del sistema).
  -->
  <div class="app-card-glass-table af-table-card">
    <!-- Encabezado de la Sección -->
    <div class="af-table-header">
      <div class="flex items-center gap-2">
        <h3 class="af-section-title mb-0">Proyectos Recientes Globales</h3>
        <span v-if="!loading && projects.length" class="af-count-badge">
          {{ projects.length }}
        </span>
      </div>
      <button class="af-link-btn" @click="$emit('view-all')">
        Ver todos
        <span class="material-symbols-outlined notranslate" style="font-size: 16px;">arrow_forward</span>
      </button>
    </div>

    <!-- State 1: Skeleton Loader (UX Cargando) -->
    <div v-if="loading" class="p-4">
      <div v-for="i in 3" :key="i" class="af-skeleton-row mb-3"></div>
    </div>

    <!-- State 2: Estado Vacío (UX No hay datos) -->
    <div v-else-if="!projects || projects.length === 0" class="af-empty-state text-center py-5">
      <span class="material-symbols-outlined notranslate af-empty-icon mb-2">folder_off</span>
      <p class="mb-1 font-bold text-slate-900">No hay proyectos recientes</p>
      <span class="text-slate-500 text-xs">Los nuevos proyectos asignados aparecerán aquí.</span>
    </div>

    <!-- State 3: Datos Presentes -->
    <template v-else>
      <!-- VISTA DESKTOP / TABLET (Tabla Tradicional) -->
      <div class="overflow-x-auto hidden md:block">
        <table class="af-table align-middle">
          <thead>
            <tr>
              <th scope="col" class="text-center" style="width: 50px;">#</th>
              <th scope="col">Proyecto</th>
              <th scope="col">Equipo / Ámbito</th>
              <th scope="col">Fecha</th>
              <th scope="col">Estado</th>
              <th scope="col" class="text-right">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(project, idx) in projects" :key="project.id || project.name" class="af-table-row">
              <td class="text-center af-index-col">{{ idx + 1 }}</td>
              <td>
                <div class="flex items-center gap-3">
                  <div class="af-project-icon" :style="{ backgroundColor: project.iconBg || 'rgba(75, 65, 225, 0.1)', color: project.iconColor || '#4b41e1' }">
                    <span class="material-symbols-outlined notranslate">{{ project.icon || 'folder' }}</span>
                  </div>
                  <div>
                    <span class="af-project-name block">{{ project.name }}</span>
                    <span v-if="project.subtitle" class="af-project-sub text-slate-500">{{ project.subtitle }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="af-team-badge">
                  <span class="material-symbols-outlined notranslate" style="font-size: 13px;">groups</span>
                  {{ project.team || 'Comunidad / Admin' }}
                </span>
              </td>
              <td>
                <span class="af-date-text">{{ project.date || 'Reciente' }}</span>
              </td>
              <td>
                <span class="af-status-pill" :class="getStatusClass(project.status)">
                  <span class="af-status-dot"></span>
                  {{ project.status }}
                </span>
              </td>
              <td class="text-right">
                <button class="af-view-btn" title="Ver detalles" @click="$emit('view-project', project)">
                  <span class="material-symbols-outlined notranslate">visibility</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- VISTA MÓVIL (Tarjetas Adaptables UX Mobile First) -->
      <div class="block md:hidden p-3">
        <div
          v-for="(project, idx) in projects"
          :key="`mobile-${project.id || project.name}`"
          class="af-mobile-card mb-3 p-3"
        >
          <div class="flex justify-between items-start mb-2">
            <div class="flex items-center gap-2">
              <div class="af-project-icon sm" :style="{ backgroundColor: project.iconBg || 'rgba(75, 65, 225, 0.1)', color: project.iconColor || '#4b41e1' }">
                <span class="material-symbols-outlined notranslate" style="font-size:16px;">{{ project.icon || 'folder' }}</span>
              </div>
              <span class="af-project-name text-base">{{ project.name }}</span>
            </div>
            <span class="af-status-pill" :class="getStatusClass(project.status)">
              <span class="af-status-dot"></span>
              {{ project.status }}
            </span>
          </div>

          <div class="flex justify-between items-center mt-3 pt-2 border-t border-slate-100 text-xs">
            <span class="af-team-badge">
              {{ project.team || 'Comunidad / Admin' }}
            </span>
            <button class="af-btn-mobile-action" @click="$emit('view-project', project)">
              <span>Detalles</span>
              <span class="material-symbols-outlined notranslate" style="font-size: 16px;">chevron_right</span>
            </button>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
export interface RecentProject {
  id?: string | number
  name: string
  subtitle?: string
  date?: string
  team?: string
  status: 'Aprobado' | 'En Revisión' | 'Rechazado' | 'Pendiente' | string
  icon?: string
  iconBg?: string
  iconColor?: string
}

withDefaults(defineProps<{
  projects: RecentProject[]
  loading?: boolean
}>(), {
  loading: false
})

defineEmits<{
  (event: 'view-all'): void
  (event: 'view-project', project: RecentProject): void
}>()

function getStatusClass(status: string) {
  const normalized = status?.toLowerCase() || ''
  if (normalized.includes('aprobado')) return 'approved'
  if (normalized.includes('rechazado')) return 'rejected'
  if (normalized.includes('revision') || normalized.includes('revisión') || normalized.includes('pendiente')) return 'review'
  return 'default'
}
</script>

<style scoped>
.material-symbols-outlined {
  vertical-align: middle;
  font-family: 'Material Symbols Outlined' !important;
}
.notranslate { -webkit-translate: no; translate: no; }

/*
  Contenedor principal hereda glassmorphism estandarizado desde
  clase utilitaria GLOBAL .app-card-glass-table (main.css:183-192).
  Los estilos locales solo agregan el overflow:hidden necesario
  para tablas. Cualquier cambio de tema se aplica desde main.css.
*/
.af-table-card {
  overflow: hidden;
}

/* Header de la Tabla */
.af-table-header {
  padding: 20px 28px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.4);
}

.af-section-title {
  font-size: 17px;
  font-weight: 800;
  color: var(--app-slate-900, #0f172a);
  letter-spacing: -0.02em;
}

.af-count-badge {
  background: rgba(75, 65, 225, 0.1);
  color: var(--app-primary, #4b41e1);
  font-size: 11px;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: var(--app-radius-pill, 9999px);
}

.af-link-btn {
  background: none;
  border: none;
  color: var(--app-primary, #4b41e1);
  font-size: 13px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
  padding: 0.35rem 0.65rem;
  border-radius: 0.5rem;
}

.af-link-btn:hover {
  background-color: rgba(75, 65, 225, 0.08);
  color: var(--app-primary-dark, #4338ca);
}

/* Tabla Desktop */
.af-table {
  width: 100%;
  margin-bottom: 0;
}

.af-table th {
  padding: 1rem 1.5rem;
  font-size: 11px;
  color: var(--app-slate-500, #64748b);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
  background: rgba(248, 250, 252, 0.5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.af-table td {
  padding: 1.1rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 14px;
}

.af-table-row {
  transition: background-color 0.2s ease;
}

.af-table-row:hover {
  background-color: rgba(75, 65, 225, 0.02);
}

.af-index-col {
  font-weight: 600;
  color: var(--app-slate-400, #94a3b8);
  font-size: 13px;
}

.af-project-icon {
  width: 36px;
  height: 36px;
  border-radius: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.6);
}

.af-project-icon.sm {
  width: 28px;
  height: 28px;
  border-radius: 0.4rem;
}

.af-project-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--app-slate-900, #0f172a);
}

.af-project-sub {
  font-size: 11px;
}

.af-team-badge {
  background: rgba(241, 245, 249, 0.8);
  color: var(--app-slate-700, #475569);
  padding: 0.3rem 0.65rem;
  font-size: 12px;
  font-weight: 600;
  border-radius: 0.5rem;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
}

.af-date-text {
  font-size: 13px;
  color: var(--app-slate-500, #64748b);
  font-weight: 500;
}

/* Status Pills — usan tokens semánticos --app-* del sistema unificado */
.af-status-pill {
  padding: 0.25rem 0.7rem;
  font-size: 11px;
  font-weight: 700;
  border-radius: var(--app-radius-pill, 9999px);
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.af-status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

.af-status-pill.approved {
  background-color: var(--app-success-bg, rgba(220, 252, 231, 0.8));
  color: var(--app-success, #15803d);
  border: 1px solid rgba(187, 247, 208, 0.8);
}

.af-status-pill.review {
  background-color: var(--app-warning-bg, rgba(254, 243, 199, 0.8));
  color: var(--app-warning, #b45309);
  border: 1px solid rgba(253, 230, 138, 0.8);
}

.af-status-pill.rejected {
  background-color: var(--app-error-bg, rgba(254, 226, 226, 0.8));
  color: var(--app-error, #b91c1c);
  border: 1px solid rgba(254, 202, 202, 0.8);
}

.af-status-pill.default {
  background-color: var(--app-slate-100, #f1f5f9);
  color: var(--app-slate-700, #475569);
  border: 1px solid var(--app-slate-200, #e2e8f0);
}

/* Botón de Acción */
.af-view-btn {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(203, 213, 225, 0.8);
  width: 34px;
  height: 34px;
  border-radius: 0.5rem;
  color: var(--app-primary, #4b41e1);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-view-btn:hover {
  background-color: var(--app-primary, #4b41e1);
  color: var(--app-on-primary, #ffffff);
  border-color: var(--app-primary, #4b41e1);
  box-shadow: 0 4px 12px rgba(75, 65, 225, 0.25);
}

/* Adaptación MÓVIL (Cards) */
.af-mobile-card {
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(226, 232, 240, 0.8);
  border-radius: 0.85rem;
  transition: background 0.2s ease;
}

.af-mobile-card:active {
  background: rgba(255, 255, 255, 0.95);
}

.af-btn-mobile-action {
  background: none;
  border: none;
  color: var(--app-primary, #4b41e1);
  font-weight: 700;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 0.1rem;
}

/* Skeletons y Estados Vacíos */
.af-empty-icon {
  font-size: 42px;
  color: var(--app-slate-300, #cbd5e1);
}

.af-skeleton-row {
  height: 48px;
  background: linear-gradient(90deg, var(--app-slate-100, #f1f5f9) 25%, var(--app-slate-200, #e2e8f0) 50%, var(--app-slate-100, #f1f5f9) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 0.5rem;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>