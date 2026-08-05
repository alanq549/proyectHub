<template>
  <div class="d-flex flex-column gap-3">
    <!-- Encabezado de Sección -->
    <div class="d-flex align-items-center justify-content-between">
      <h3 class="af-section-title d-flex align-items-center gap-2 mb-0">
        <span class="material-symbols-outlined notranslate af-title-icon">event_available</span>
        Convocatorias Vigentes
      </h3>
      <span v-if="!loading && calls?.length" class="af-count-pill">
        {{ calls.length }} {{ calls.length === 1 ? 'activa' : 'activas' }}
      </span>
    </div>

    <!-- State 1: Skeleton Loading (UX Cargando) -->
    <div v-if="loading" class="row g-3">
      <div v-for="i in 2" :key="i" class="col-12 col-md-6">
        <div class="app-card-glass-light af-call-card p-4">
          <div class="af-skeleton-line w-75 mb-2"></div>
          <div class="af-skeleton-line w-100 mb-1"></div>
          <div class="af-skeleton-line w-50 mb-4"></div>
          <div class="d-flex justify-content-between align-items-center mt-auto">
            <div class="af-skeleton-line w-25"></div>
            <div class="af-skeleton-button"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- State 2: Estado Vacío (UX Sin Convocatorias) -->
    <div v-else-if="!calls || calls.length === 0" class="app-card-glass-light text-center py-5">
      <span class="material-symbols-outlined notranslate af-empty-icon mb-2">event_busy</span>
      <p class="mb-1 fw-bold text-dark">No hay convocatorias vigentes</p>
      <span class="text-muted small">Las nuevas aperturas de proyectos y becas se publicarán aquí.</span>
    </div>

    <!-- State 3: Lista de Convocatorias -->
    <div v-else class="row g-3">
      <div class="col-12 col-md-6" v-for="call in calls" :key="call.id || call.title">
        <div class="app-card-glass-light af-call-card">
          <!-- Cabecera de la Card: Título + Badge de Organización -->
          <div>
            <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
              <h4 class="af-call-title mb-0">{{ call.title }}</h4>
              <span
                class="af-call-org flex-shrink-0"
                :style="{
                  backgroundColor: call.orgBg || 'rgba(75, 65, 225, 0.1)',
                  color: call.orgColor || 'var(--app-primary)'
                }"
              >
                {{ call.org }}
              </span>
            </div>

            <p class="af-call-desc mb-0">{{ call.description }}</p>
          </div>

          <!-- Pie de la Card: Fecha Límite + Botón de Acción -->
          <div class="d-flex align-items-center justify-content-between mt-4 pt-2 border-top border-light-subtle">
            <div class="d-flex align-items-center gap-2">
              <div class="af-deadline-icon-wrapper">
                <span class="material-symbols-outlined notranslate">schedule</span>
              </div>
              <div class="d-flex flex-column">
                <span class="af-call-deadline-label">Fecha Límite</span>
                <span class="af-call-deadline-value">{{ call.deadline }}</span>
              </div>
            </div>

            <button 
              class="af-btn-primary sm d-inline-flex align-items-center gap-1"
              @click="$emit('apply', call)"
            >
              <span>Postular</span>
              <span class="material-symbols-outlined notranslate" style="font-size: 16px;">send</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface ActiveCall {
  id?: string | number
  title: string
  org: string
  orgBg?: string
  orgColor?: string
  description: string
  deadline: string
}

withDefaults(defineProps<{
  calls: ActiveCall[]
  loading?: boolean
}>(), {
  loading: false
})

defineEmits<{
  (event: 'apply', call: ActiveCall): void
}>()
</script>

<style scoped>
.material-symbols-outlined {
  vertical-align: middle;
  font-family: 'Material Symbols Outlined' !important;
}
.notranslate { -webkit-translate: no; translate: no; }

/* Título e Íconos de Sección */
.af-section-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--app-on-surface, #0f172a);
  letter-spacing: -0.02em;
}

.af-title-icon {
  color: var(--app-primary, #4b41e1);
  font-size: 22px;
}

.af-count-pill {
  background: var(--app-glass-bg-hover, rgba(255, 255, 255, 0.8));
  border: 1px solid var(--app-glass-border, rgba(255, 255, 255, 0.6));
  color: var(--app-primary, #4b41e1);
  font-size: 11px;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 9999px;
}

/* Layout Interno de la Card (El Glassmorphism lo da .app-card-glass-light) */
.af-call-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 20px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.af-call-card:hover {
  transform: translateY(-2px);
}

.af-call-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--app-on-surface, #0f172a);
  line-height: 1.3;
}

.af-call-org {
  padding: 0.25rem 0.6rem;
  font-size: 10px;
  border-radius: 0.375rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.af-call-desc {
  font-size: 13px;
  color: var(--app-slate-600, #475569);
  line-height: 1.45;
  margin-top: 6px;
}

/* Sección Fecha Límite */
.af-deadline-icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--app-error, #ef4444);
  display: flex;
  align-items: center;
  justify-content: center;
}

.af-deadline-icon-wrapper .material-symbols-outlined {
  font-size: 18px;
}

.af-call-deadline-label {
  font-size: 10px;
  color: var(--app-slate-500, #64748b);
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
  line-height: 1;
}

.af-call-deadline-value {
  font-size: 13px;
  color: var(--app-error, #ef4444);
  font-weight: 700;
}

/* Botón Principal Adaptado al Sistema de Tokens */
.af-btn-primary {
  background-color: var(--app-primary, #4b41e1);
  color: #ffffff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.6rem;
  font-size: 13px;
  font-weight: 700;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 4px 12px rgba(75, 65, 225, 0.25);
  cursor: pointer;
}

.af-btn-primary:hover {
  opacity: 0.92;
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(75, 65, 225, 0.35);
  color: #ffffff;
}

.af-btn-primary:active {
  transform: translateY(0);
}

.af-btn-primary.sm { 
  padding: 0.4rem 0.85rem; 
}

/* Skeleton & Empty States */
.af-empty-icon {
  font-size: 42px;
  color: var(--app-slate-400, #94a3b8);
}

.af-skeleton-line {
  height: 14px;
  background: linear-gradient(90deg, rgba(0,0,0,0.04) 25%, rgba(0,0,0,0.08) 50%, rgba(0,0,0,0.04) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 0.375rem;
}

.af-skeleton-button {
  height: 32px;
  width: 90px;
  background: linear-gradient(90deg, rgba(0,0,0,0.04) 25%, rgba(0,0,0,0.08) 50%, rgba(0,0,0,0.04) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border-radius: 0.5rem;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>