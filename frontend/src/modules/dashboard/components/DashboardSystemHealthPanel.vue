<template>
  <!--
    DashboardSystemHealthPanel — Bloque 1.6b (Migración Bootstrap → Tailwind)
    • 6 utilidades d-flex / gap / mb-* / justify-between migradas.
    • .app-card-glass-light global intacta, clases locales para tipografía
      métricas / progress intactas (usan tokens --app-surface-container-*).
  -->
  <div class="app-card-glass-light af-panel-card">
    <h3 class="af-section-title mb-4">Estado del Sistema</h3>
    <div class="flex flex-col gap-4">
      <div v-for="metric in metrics" :key="metric.label">
        <div class="flex justify-between mb-2">
          <span class="af-metric-label">{{ metric.label }}</span>
          <span class="af-metric-value">{{ metric.value }}</span>
        </div>
        <div class="af-progress-track">
          <div class="af-progress-fill" :style="{ width: metric.percent + '%' }"></div>
        </div>
      </div>

      <div>
        <div class="flex justify-between mb-2">
          <span class="af-metric-label">Buckets en S3</span>
          <span class="af-metric-value neutral">{{ bucketsActive }} Activos</span>
        </div>
        <div class="flex gap-1">
          <div
            v-for="n in totalBuckets"
            :key="n"
            class="af-bucket-segment"
            :class="{
              filled: n <= bucketsActive,
              'rounded-start': n === 1,
              'rounded-end': n === totalBuckets
            }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface SystemMetric {
  label: string
  value: string
  percent: number
}

defineProps<{
  metrics: SystemMetric[]
  bucketsActive: number
  totalBuckets: number
}>()
</script>

<style scoped>
/*
  Contenedor principal usa la clase GLOBAL .app-card-glass-light
  (main.css), por lo que aquí no re-declaramos bg/blur/border/padding.
  Solo aplicamos overrides internos si fuera necesario.
*/
.af-panel-card {
  padding: 24px; /* Override: S3/SystemHealth necesita 24px en lugar de 20px default glass-light */
}

.af-section-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--app-black, #000);
}

.af-metric-label {
  font-size: 14px;
  color: var(--app-on-surface, #191c1e);
}

.af-metric-value {
  font-size: 14px;
  color: var(--app-success, #16a34a);
  font-weight: 700;
}

.af-metric-value.neutral {
  color: var(--app-on-surface-variant, #45464d);
}

.af-progress-track {
  height: 6px;
  width: 100%;
  background-color: var(--app-surface-container-highest, #e0e3e5);
  border-radius: var(--app-radius-pill, 9999px);
  overflow: hidden;
}

.af-progress-fill {
  height: 100%;
  background-color: #22c55e;
  border-radius: var(--app-radius-pill, 9999px);
}

.af-bucket-segment {
  height: 8px;
  flex-grow: 1;
  background-color: var(--app-surface-container-highest, #e0e3e5);
}

.af-bucket-segment.filled {
  background-color: var(--app-primary, #4b41e1);
}

.rounded-start { border-top-left-radius: 9999px; border-bottom-left-radius: 9999px; }
.rounded-end   { border-top-right-radius: 9999px; border-bottom-right-radius: 9999px; }
</style>
