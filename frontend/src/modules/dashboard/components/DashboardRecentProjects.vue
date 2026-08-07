<template>
  <!--
    DashboardRecentProjects — Bloque 1.4 (Migración Bootstrap → Tailwind)
    • Integrado al sistema de tokens `main.css` mediante la clase .app-card-glass-table
    • Estilos de estado y badges sincronizados con las variables de tema global
  -->
  <div class="app-card-glass-table af-table-card">
    <!-- Encabezado de la Sección -->
    <div class="af-table-header">
      <div class="tw-flex tw-items-center tw-gap-2">
        <h3 class="af-section-title tw-mb-0">Proyectos Recientes Globales</h3>
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
    <div v-if="loading" class="tw-p-4">
      <div v-for="i in 3" :key="i" class="af-skeleton-row tw-mb-3"></div>
    </div>

    <!-- State 2: Estado Vacío (UX No hay datos) -->
    <div v-else-if="!projects || projects.length === 0" class="af-empty-state tw-text-center tw-py-8">
      <span class="material-symbols-outlined notranslate af-empty-icon tw-mb-2">folder_off</span>
      <p class="tw-mb-1 tw-font-bold tw-text-slate-900">No hay proyectos recientes</p>
      <span class="tw-text-slate-500 tw-text-xs">Los nuevos proyectos asignados aparecerán aquí.</span>
    </div>

    <!-- State 3: Datos Presentes -->
    <template v-else>
      <!-- VISTA DESKTOP / TABLET (Tabla Tradicional) -->
      <div class="tw-overflow-x-auto tw-hidden md:tw-block">
        <table class="af-table tw-align-middle">
          <thead>
            <tr>
              <th scope="col" class="tw-text-center" style="width: 50px;">#</th>
              <th scope="col">Proyecto</th>
              <th scope="col">Equipo / Ámbito</th>
              <th scope="col">Fecha</th>
              <th scope="col">Estado</th>
              <th scope="col" class="tw-text-right">Acción</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(project, idx) in projects" :key="project.id || project.name" class="af-table-row">
              <td class="tw-text-center af-index-col">{{ idx + 1 }}</td>
              <td>
                <div class="tw-flex tw-items-center tw-gap-3">
                  <div 
                    class="af-project-icon"
                    :style="{ 
                      backgroundColor: project.iconBg || 'rgba(15, 23, 42, 0.08)', 
                      color: project.iconColor || 'var(--app-primary)' 
                    }"
                  >
                    <span class="material-symbols-outlined notranslate">{{ project.icon || 'folder' }}</span>
                  </div>
                  <div>
                    <span class="af-project-name tw-block">{{ project.name }}</span>
                    <span v-if="project.subtitle" class="af-project-sub tw-text-slate-500">{{ project.subtitle }}</span>
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
              <td class="tw-text-right">
                <button class="af-view-btn" title="Ver detalles" @click="$emit('view-project', project)">
                  <span class="material-symbols-outlined notranslate">visibility</span>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- VISTA MÓVIL (Tarjetas Adaptables UX Mobile First) -->
      <div class="tw-block md:tw-hidden tw-p-3">
        <div 
          v-for="project in projects" 
          :key="`mobile-${project.id || project.name}`"
          class="af-mobile-card tw-mb-3 tw-p-3"
        >
          <div class="tw-flex tw-justify-between tw-items-start tw-mb-2">
            <div class="tw-flex tw-items-center tw-gap-2">
              <div 
                class="af-project-icon sm"
                :style="{ 
                  backgroundColor: project.iconBg || 'rgba(15, 23, 42, 0.08)', 
                  color: project.iconColor || 'var(--app-primary)' 
                }"
              >
                <span class="material-symbols-outlined notranslate" style="font-size:16px;">
                  {{ project.icon || 'folder' }}
                </span>
              </div>
              <span class="af-project-name tw-text-base">{{ project.name }}</span>
            </div>
            <span class="af-status-pill" :class="getStatusClass(project.status)">
              <span class="af-status-dot"></span>
              {{ project.status }}
            </span>
          </div>

          <div class="tw-flex tw-justify-between tw-items-center tw-mt-3 tw-pt-2 tw-border-t tw-border-slate-200/60 tw-text-xs">
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

.notranslate {
  -webkit-translate: no;
  translate: no;
}

.af-table-card {
  overflow: hidden;
}

/* Header de la Tabla */
.af-table-header {
  padding: 18px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.4);
}

.af-section-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--app-slate-900, #0f172a);
  letter-spacing: -0.02em;
}

.af-count-badge {
  background: rgba(15, 23, 42, 0.08);
  color: var(--app-primary, #0f172a);
  font-size: 11px;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: var(--app-radius-pill, 9999px);
}

.af-link-btn {
  background: none;
  border: none;
  color: var(--app-primary, #0f172a);
  font-size: 13px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.2s ease;
  padding: 0.35rem 0.65rem;
  border-radius: 0.5rem;
  cursor: pointer;
}

.af-link-btn:hover {
  background-color: rgba(15, 23, 42, 0.06);
  color: var(--app-black, #000000);
}

/* Tabla Desktop */
.af-table {
  width: 100%;
  margin-bottom: 0;
  border-collapse: collapse;
}

.af-table th {
  padding: 0.85rem 1.25rem;
  font-size: 11px;
  color: var(--app-slate-500, #64748b);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 700;
  background: rgba(248, 250, 252, 0.5);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.af-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 14px;
}

.af-table-row {
  transition: background-color 0.2s ease;
}

.af-table-row:hover {
  background-color: rgba(15, 23, 42, 0.02);
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

/* Status Pills — Usan tokens semánticos --app-* */
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
  color: var(--app-error, #ba1a1a);
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
  color: var(--app-primary, #0f172a);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-view-btn:hover {
  background-color: var(--app-primary, #0f172a);
  color: var(--app-on-primary, #ffffff);
  border-color: var(--app-primary, #0f172a);
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}

/* Adaptación MÓVIL (Cards) */
.af-mobile-card {
  background: rgba(255, 255, 255, 0.75);
  border: 1px solid rgba(226, 232, 240, 0.9);
  border-radius: 0.85rem;
  transition: background 0.2s ease;
}

.af-mobile-card:active {
  background: rgba(255, 255, 255, 0.95);
}

.af-btn-mobile-action {
  background: none;
  border: none;
  color: var(--app-primary, #0f172a);
  font-weight: 700;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 0.1rem;
  cursor: pointer;
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
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>