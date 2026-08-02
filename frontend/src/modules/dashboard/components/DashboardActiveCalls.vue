<template>
  <div class="d-flex flex-column gap-3">
    <h3 class="af-section-title d-flex align-items-center gap-2">
      <span class="material-symbols-outlined notranslate" style="color: var(--af-secondary, #4b41e1);">event_available</span>
      Convocatorias Vigentes
    </h3>
    <div class="row g-3">
      <div class="col-12 col-md-6" v-for="call in calls" :key="call.title">
        <div class="af-call-card">
          <div>
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h4 class="af-call-title mb-0">{{ call.title }}</h4>
              <span
                class="af-call-org"
                :style="{ backgroundColor: call.orgBg, color: call.orgColor }"
              >{{ call.org }}</span>
            </div>
            <p class="af-call-desc mb-0">{{ call.description }}</p>
          </div>
          <div class="d-flex align-items-center justify-content-between mt-4">
            <div class="d-flex flex-column">
              <span class="af-call-deadline-label">Límite</span>
              <span class="af-call-deadline-value">{{ call.deadline }}</span>
            </div>
            <button class="af-btn-secondary sm" @click="$emit('apply', call)">Postular</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
export interface ActiveCall {
  title: string
  org: string
  orgBg: string
  orgColor: string
  description: string
  deadline: string
}

defineProps<{
  calls: ActiveCall[]
}>()

defineEmits<{
  (event: 'apply', call: ActiveCall): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

.af-section-title { font-size: 20px; font-weight: 600; color: var(--af-primary, #000); }

.af-call-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 20px;
  border-radius: 0.75rem;
  border: 1px solid rgba(198, 198, 205, 0.3);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  transition: box-shadow .2s ease;
}
.af-call-card:hover { box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
.af-call-title { font-size: 16px; font-weight: 700; color: var(--af-primary, #000); }
.af-call-org { padding: 0.25rem 0.5rem; font-size: 10px; border-radius: 0.25rem; font-weight: 700; }
.af-call-desc { font-size: 12px; color: var(--af-on-surface-variant, #45464d); }
.af-call-deadline-label { font-size: 10px; color: var(--af-on-surface-variant, #45464d); text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; }
.af-call-deadline-value { font-size: 14px; color: var(--af-error, #ba1a1a); font-weight: 700; }
.af-btn-secondary {
  background-color: var(--af-secondary, #4b41e1);
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 14px;
  transition: opacity .15s ease;
  box-shadow: 0 10px 15px -3px rgba(75,65,225,0.2);
}
.af-btn-secondary:hover { opacity: 0.9; color: #fff; }
.af-btn-secondary.sm { padding: 0.4rem 1rem; }
</style>
