<template>
  <!--
    DashboardKpiGrid — Bloque 1.3 (Migración Bootstrap → Tailwind)
    • Layout row/col → grid responsive (4 cols desktop / 2 tablet / 1 móvil).
    • Clase glass .app-card-glass GLOBAL intacta (solo override padding KPI 22/24 px).
    • Todas utilidades espaciado/flex migradas (ms-auto = ms-auto, etc.).
  -->
  <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
    <div v-for="kpi in kpis" :key="kpi.label">
      <div class="app-card-glass af-kpi-card">
        <!-- Glow suave de fondo en hover -->
        <div class="af-kpi-bg-glow" :style="{ background: kpi.iconColor }"></div>

        <!-- Encabezado de la card: Label + Ícono -->
        <div class="flex justify-between items-center">
          <span class="af-kpi-label">{{ kpi.label }}</span>
          <div class="af-kpi-icon" :style="{ backgroundColor: kpi.iconBg, color: kpi.iconColor }">
            <span class="material-symbols-outlined notranslate">{{ kpi.icon }}</span>
          </div>
        </div>

        <!-- Valor Principal -->
        <div class="af-kpi-value-container my-1">
          <h3 class="af-kpi-value mb-0">
            {{ kpi.value }}
            <span v-if="kpi.unit" class="af-kpi-unit">{{ kpi.unit }}</span>
          </h3>
        </div>

        <!-- Barra de Progreso Opcional (UX) -->
        <div v-if="kpi.progress !== undefined" class="af-progress-container mt-2">
          <div class="af-progress-bar">
            <div
              class="af-progress-fill"
              :style="{ width: `${kpi.progress}%`, background: kpi.iconColor }"
            ></div>
          </div>
        </div>

        <!-- Pie de la Card / Metadatos Contextuales -->
        <div class="af-kpi-footer flex items-center justify-between mt-auto pt-2">
          <!-- Tendencia (Ej: +12%) -->
          <span v-if="kpi.trend" class="af-kpi-trend">
            <span class="material-symbols-outlined notranslate" style="font-size: 16px;">trending_up</span>
            {{ kpi.trend }}
          </span>

          <!-- Tag / Estado -->
          <span v-else-if="kpi.tag" class="af-kpi-tag" :style="{ color: kpi.iconColor, backgroundColor: kpi.iconBg }">
            {{ kpi.tag }}
          </span>

          <!-- Desglose (Ej: 30 Aprobados / 15 Revisión) -->
          <div v-else-if="kpi.breakdown" class="flex items-center gap-2">
            <span class="af-kpi-breakdown-positive">{{ kpi.breakdown.positive }}</span>
            <span class="af-kpi-bullet">•</span>
            <span class="af-kpi-breakdown-neutral">{{ kpi.breakdown.neutral }}</span>
          </div>

          <!-- Nota al pie -->
          <span v-else-if="kpi.footnote" class="af-kpi-footnote">{{ kpi.footnote }}</span>

          <span v-if="kpi.subtext" class="af-kpi-subtext ms-auto">{{ kpi.subtext }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
export interface KpiBreakdown { positive: string; neutral: string }

export interface Kpi {
  label: string
  value: string
  icon: string
  iconBg: string
  iconColor: string
  trend?: string
  tag?: string
  breakdown?: KpiBreakdown
  footnote?: string
  unit?: string
  progress?: number // Porcentaje (0 a 100) para barra de progreso
  subtext?: string
}

defineProps<{
  kpis: Kpi[]
}>()
</script>

<style scoped>
.material-symbols-outlined { 
  vertical-align: middle; 
  font-family: 'Material Symbols Outlined' !important; 
}
.notranslate { -webkit-translate: no; translate: no; }

/*
  Contenedor principal hereda glassmorphism estandarizado desde
  clase utilitaria global .app-card-glass (main.css).
  Estilos locales solo agregan: internal layout specifics (flex, overflow),
  glow hover esquina, tipografía específica KPI, progress bar y footer chips.
*/
.af-kpi-card {
  overflow: hidden;
  /* Override padding default glass ya que KPI necesita menos padding 22→24 */
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  height: 100%;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
/* Re-define hover: glass da uno, pero KPI agrega translateY y glow sutil */
.af-kpi-card:hover {
  transform: translateY(-3px);
}

/* Destello sutil en esquina al pasar el ratón */
.af-kpi-bg-glow {
  position: absolute;
  top: -30px;
  right: -30px;
  width: 100px;
  height: 100px;
  opacity: 0;
  border-radius: 50%;
  filter: blur(25px);
  transition: opacity 0.3s ease;
  pointer-events: none;
}

.af-kpi-card:hover .af-kpi-bg-glow {
  opacity: 0.15;
}

/* Tipografías e Íconos */
.af-kpi-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--app-slate-500, #64748b);
  letter-spacing: -0.01em;
}

.af-kpi-icon {
  width: 38px;
  height: 38px;
  border-radius: var(--app-glass-radius-sm, 0.75rem);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.5);
}

.af-kpi-value {
  font-size: 30px;
  font-weight: 800;
  color: var(--app-slate-900, #0f172a);
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.af-kpi-unit {
  font-size: 18px;
  font-weight: 600;
  color: var(--app-slate-500, #64748b);
  margin-left: 2px;
}

/* Barra de Progreso UX */
.af-progress-container {
  width: 100%;
}

.af-progress-bar {
  width: 100%;
  height: 6px;
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: 9999px;
  overflow: hidden;
}

.af-progress-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.5s ease-out;
}

/* Elementos del Footer */
.af-kpi-footer {
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  font-size: 12px;
}

.af-kpi-trend {
  color: var(--app-success, #16a34a);
  background-color: rgba(220, 252, 231, 0.7);
  padding: 0.15rem 0.5rem;
  border-radius: var(--app-radius-pill, 9999px);
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 11px;
}

.af-kpi-tag {
  padding: 0.2rem 0.6rem;
  font-size: 11px;
  border-radius: 0.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.af-kpi-breakdown-positive {
  font-weight: 700;
  color: var(--app-success, #16a34a);
  font-size: 11px;
}

.af-kpi-bullet {
  color: var(--app-slate-300, #cbd5e1);
  font-size: 10px;
}

.af-kpi-breakdown-neutral {
  font-size: 11px;
  color: var(--app-slate-500, #64748b);
  font-weight: 600;
}

.af-kpi-footnote {
  font-size: 11px;
  color: var(--app-slate-500, #64748b);
  font-weight: 500;
}

.af-kpi-subtext {
  font-size: 11px;
  color: var(--app-slate-400, #94a3b8);
}
</style>