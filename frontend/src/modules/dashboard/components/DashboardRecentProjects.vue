<template>
  <div class="af-table-card">
    <div class="af-table-header">
      <h3 class="af-section-title mb-0">Proyectos Recientes</h3>
      <button class="af-link-btn" @click="$emit('view-all')">Ver todos</button>
    </div>
    <div class="table-responsive">
      <table class="af-table">
        <thead>
          <tr>
            <th>Proyecto</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="project in projects" :key="project.name">
            <td>
              <div class="d-flex align-items-center gap-3">
                <div class="af-project-icon" :style="{ backgroundColor: project.iconBg }">
                  <span class="material-symbols-outlined notranslate" style="font-size:20px;">{{ project.icon }}</span>
                </div>
                <span class="af-project-name">{{ project.name }}</span>
              </div>
            </td>
            <td class="af-project-date">{{ project.date }}</td>
            <td>
              <span
                class="af-status-pill"
                :class="project.status === 'Aprobado' ? 'approved' : 'review'"
              >{{ project.status }}</span>
            </td>
            <td class="text-end">
              <button class="af-view-btn" @click="$emit('view-project', project)">
                <span class="material-symbols-outlined notranslate">visibility</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface RecentProject {
  name: string
  date: string
  status: 'Aprobado' | 'En Revisión' | string
  icon: string
  iconBg: string
}

defineProps<{
  projects: RecentProject[]
}>()

defineEmits<{
  (event: 'view-all'): void
  (event: 'view-project', project: RecentProject): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

.af-table-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: 0.75rem;
  border: 1px solid rgba(198, 198, 205, 0.3);
  box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.04), 0px 2px 4px rgba(0, 0, 0, 0.02);
  overflow: hidden;
}
.af-table-header {
  padding: 24px;
  border-bottom: 1px solid rgba(198, 198, 205, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: rgba(255,255,255,0.5);
}
.af-section-title { font-size: 20px; font-weight: 600; color: var(--af-primary, #000); }
.af-link-btn {
  background: none;
  border: none;
  color: var(--af-secondary, #4b41e1);
  font-size: 14px;
}
.af-link-btn:hover { text-decoration: underline; }

.af-table { width: 100%; text-align: left; border-collapse: collapse; margin-bottom: 0; }
.af-table thead { background-color: rgba(242, 244, 246, 0.5); }
.af-table th {
  padding: 1rem 1.5rem;
  font-size: 14px;
  color: var(--af-on-surface-variant, #45464d);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}
.af-table td { padding: 1.25rem 1.5rem; border-top: 1px solid rgba(198,198,205,0.1); vertical-align: middle; }
.af-table tbody tr { transition: background-color .15s ease; }
.af-table tbody tr:hover { background-color: var(--af-surface-container-low, #f2f4f6); }
.af-table tbody tr:hover .af-view-btn { opacity: 1; }

.af-project-icon {
  width: 32px; height: 32px;
  border-radius: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}
.af-project-name { font-size: 16px; font-weight: 600; color: var(--af-primary, #000); }
.af-project-date { font-size: 12px; color: var(--af-on-surface-variant, #45464d); }
.af-status-pill {
  padding: 0.25rem 0.75rem;
  font-size: 10px;
  font-weight: 700;
  border-radius: 9999px;
}
.af-status-pill.approved { background-color: #f0fdf4; color: #15803d; border: 1px solid #dcfce7; }
.af-status-pill.review { background-color: #fff7ed; color: #c2410c; border: 1px solid #ffedd5; }
.af-view-btn {
  opacity: 0;
  transition: opacity .15s ease;
  background: none;
  border: none;
  padding: 0.5rem;
  border-radius: 50%;
  color: var(--af-secondary, #4b41e1);
}
.af-view-btn:hover { background-color: rgba(75,65,225,0.1); }
</style>
