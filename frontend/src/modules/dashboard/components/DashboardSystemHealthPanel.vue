<template>
  <div class="af-panel-card">
    <h3 class="af-section-title mb-4">Estado del Sistema</h3>
    <div class="d-flex flex-column gap-4">
      <div v-for="metric in metrics" :key="metric.label">
        <div class="d-flex justify-content-between mb-2">
          <span class="af-metric-label">{{ metric.label }}</span>
          <span class="af-metric-value">{{ metric.value }}</span>
        </div>
        <div class="af-progress-track">
          <div class="af-progress-fill" :style="{ width: metric.percent + '%' }"></div>
        </div>
      </div>

      <div>
        <div class="d-flex justify-content-between mb-2">
          <span class="af-metric-label">Buckets en S3</span>
          <span class="af-metric-value neutral">{{ bucketsActive }} Activos</span>
        </div>
        <div class="d-flex gap-1">
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
.af-panel-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 24px;
  border-radius: 0.75rem;
  border: 1px solid rgba(198, 198, 205, 0.3);
  box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.04), 0px 2px 4px rgba(0, 0, 0, 0.02);
}
.af-section-title { font-size: 20px; font-weight: 600; color: var(--af-primary, #000); }

.af-metric-label { font-size: 14px; color: var(--af-on-surface, #191c1e); }
.af-metric-value { font-size: 14px; color: #16a34a; font-weight: 700; }
.af-metric-value.neutral { color: var(--af-on-surface-variant, #45464d); }
.af-progress-track { height: 6px; width: 100%; background-color: var(--af-surface-container-highest, #e0e3e5); border-radius: 9999px; overflow: hidden; }
.af-progress-fill { height: 100%; background-color: #22c55e; border-radius: 9999px; }
.af-bucket-segment {
  height: 8px;
  flex-grow: 1;
  background-color: var(--af-surface-container-highest, #e0e3e5);
}
.af-bucket-segment.filled { background-color: var(--af-secondary, #4b41e1); }
.rounded-start { border-top-left-radius: 9999px; border-bottom-left-radius: 9999px; }
.rounded-end { border-top-right-radius: 9999px; border-bottom-right-radius: 9999px; }
</style>
