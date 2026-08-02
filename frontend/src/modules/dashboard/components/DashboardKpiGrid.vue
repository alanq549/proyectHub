<template>
  <section class="row g-4 mb-4">
    <div class="col-12 col-sm-6 col-lg-3" v-for="kpi in kpis" :key="kpi.label">
      <div class="af-kpi-card">
        <div class="d-flex justify-content-between align-items-start">
          <div class="af-kpi-icon" :style="{ backgroundColor: kpi.iconBg, color: kpi.iconColor }">
            <span class="material-symbols-outlined notranslate">{{ kpi.icon }}</span>
          </div>
          <span v-if="kpi.trend" class="af-kpi-trend">
            <span class="material-symbols-outlined notranslate" style="font-size:18px;">trending_up</span>
            {{ kpi.trend }}
          </span>
          <span v-else-if="kpi.tag" class="af-kpi-tag">{{ kpi.tag }}</span>
          <div v-else-if="kpi.breakdown" class="d-flex flex-column text-end">
            <span class="af-kpi-breakdown-positive">{{ kpi.breakdown.positive }}</span>
            <span class="af-kpi-breakdown-neutral">{{ kpi.breakdown.neutral }}</span>
          </div>
          <span v-else-if="kpi.footnote" class="af-kpi-footnote">{{ kpi.footnote }}</span>
        </div>
        <div>
          <p class="af-kpi-label">{{ kpi.label }}</p>
          <p class="af-kpi-value">
            {{ kpi.value }}
            <span v-if="kpi.unit" class="af-kpi-unit">{{ kpi.unit }}</span>
          </p>
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
}

defineProps<{
  kpis: Kpi[]
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

.af-kpi-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 24px;
  border-radius: 0.75rem;
  border: 1px solid rgba(198, 198, 205, 0.3);
  box-shadow: 0px 10px 30px rgba(79, 70, 229, 0.04), 0px 2px 4px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 100%;
}
.af-kpi-icon {
  padding: 0.75rem;
  border-radius: 0.5rem;
  display: inline-flex;
}
.af-kpi-trend { color: #16a34a; font-weight: 700; display: flex; align-items: center; font-size: 14px; }
.af-kpi-tag {
  padding: 0.125rem 0.5rem;
  background-color: rgba(172,237,255,0.2);
  color: var(--af-on-tertiary-fixed-variant, #004e5c);
  font-size: 10px;
  border-radius: 0.375rem;
  font-weight: 700;
  text-transform: uppercase;
}
.af-kpi-breakdown-positive { font-size: 10px; color: #16a34a; font-weight: 700; }
.af-kpi-breakdown-neutral { font-size: 10px; color: var(--af-on-surface-variant, #45464d); }
.af-kpi-footnote { font-size: 10px; color: var(--af-on-surface-variant, #45464d); font-weight: 500; }
.af-kpi-label { font-size: 12px; color: var(--af-on-surface-variant, #45464d); margin-bottom: 0; }
.af-kpi-value { font-size: 32px; font-weight: 700; color: var(--af-primary, #000); margin-bottom: 0; }
.af-kpi-unit { font-size: 20px; }
</style>
