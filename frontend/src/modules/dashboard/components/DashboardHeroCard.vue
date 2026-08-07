<template>
  <!--
    DashboardHeroCard — Bloque 1.2 (Migración Bootstrap → Tailwind)
    • Clase glassmorphism .app-card-glass-xl GLOBAL de main.css intacta (transición).
    • Utilidades Bootstrap (text-start / d-flex / mt-* / align-items-*) migradas a *.
    • Botones mantienen clases locales af-btn-* (son estilos custom, no Bootstrap).
  -->
  <AppCard variant="glass-xl" padding="none" class=" af-hero-card">
    <div class="af-hero-glow"></div>
    <div class="af-hero-body">
      <div class="af-hero-left">
        <div class="af-avatar-wrapper">
          <UserAvatar
            :src="user.avatarUrl"
            :alt="`Perfil ${user.name}`"
            size="lg"
          />
        </div>
        <div class="tw-text-left">
          <h2 class="af-hero-title notranslate">¡Hola de nuevo, {{ user.name }}! 👋</h2>
          <div class="tw-flex tw-items-center tw-gap-2 tw-mt-2 tw-flex-wrap">
            <span class="af-role-badge">{{ user.role }}</span>
            <span class="af-secure-badge">
              <span class="material-symbols-outlined notranslate" style="font-size:14px;">lock</span>
              Conexión Segura
            </span>
          </div>
        </div>
      </div>

      <div class="tw-flex tw-flex-wrap tw-gap-2 tw-mt-3 md:tw-mt-0 tw-items-center">
        <button class="af-btn-primary" @click="$emit('manage-users')">
          <span class="material-symbols-outlined notranslate" style="font-size: 18px;">manage_accounts</span>
          Gestionar Usuarios
        </button>
        <button class="af-btn-outline" @click="$emit('download-report')">
          <span class="material-symbols-outlined notranslate" style="font-size: 18px;">download</span>
          Descargar Reporte
        </button>
        <button class="af-btn-black" @click="$emit('new-audit')">
          <span class="material-symbols-outlined notranslate" style="font-size: 18px;">add</span>
          Nueva Auditoría
        </button>
      </div>
    </div>
  </AppCard>
</template>

<script setup lang="ts">
import AppCard from '@/shared/components/AppCard.vue'

import UserAvatar from '@/layouts/components/UserAvatar.vue'

export interface DashboardHeroUser {
  name: string
  role: string
  avatarUrl: string
}

defineProps<{
  user: DashboardHeroUser
}>()

defineEmits<{
  (event: 'download-report'): void
  (event: 'new-audit'): void
  (event: 'manage-users'): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

/*
  El contenedor principal AHORA hereda glassmorphism de la clase global
  .app-card-glass-xl definida en main.css (background, blur, border, shadow,
  radius, padding, hover). El estilo local solo agrega:
    - Degradé especial en el fondo (sobre-escribe el glass-bg por defecto)
    - Gradiente glow esquina
*/
.af-hero-card {
  background: linear-gradient(
    135deg, 
    rgba(255, 255, 255, 0.85) 0%, 
    rgba(245, 247, 255, 0.75) 60%, 
    rgba(235, 233, 254, 0.6) 100%
  );
}

/* Destello sutil de fondo */
.af-hero-glow {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(75, 65, 225, 0.15) 0%, rgba(255, 255, 255, 0) 70%);
  pointer-events: none;
  border-radius: 50%;
}

.af-hero-body {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .af-hero-body {
    flex-direction: row;
    align-items: center;
  }
}

.af-hero-left {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.af-avatar-wrapper {
  position: relative;
  border-radius: 50%;
  padding: 3px;
  background: linear-gradient(135deg, rgba(75, 65, 225, 0.3) 0%, rgba(255, 255, 255, 0.8) 100%);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.af-hero-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--app-slate-900, #0f172a);
  margin: 0;
  letter-spacing: -0.02em;
}

/* Badges con diseño neumórfico/soft */
.af-role-badge {
  background: rgba(75, 65, 225, 0.08);
  color: var(--app-primary, #4b41e1);
  border: 1px solid rgba(75, 65, 225, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: var(--app-radius-pill, 9999px);
  font-size: 12px;
  font-weight: 700;
  backdrop-filter: blur(4px);
}

.af-secure-badge {
  padding: 0.25rem 0.75rem;
  background-color: var(--app-success-bg, rgba(220, 252, 231, 0.8));
  color: var(--app-success, #15803d);
  font-size: 12px;
  font-weight: 700;
  border-radius: var(--app-radius-pill, 9999px);
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  border: 1px solid rgba(187, 247, 208, 0.8);
  backdrop-filter: blur(4px);
}

/* Estilos de Botones — tokens --app-btn-* */
.af-btn-primary {
  background: var(--app-btn-primary-bg, linear-gradient(135deg, #5b50f6 0%, #4b41e1 100%));
  color: var(--app-on-primary, #ffffff);
  border: none;
  height: var(--app-btn-primary-height, 42px);
  padding: 0 1.25rem;
  border-radius: var(--app-btn-radius-md, 0.75rem);
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  box-shadow: var(--app-btn-primary-shadow, 0 4px 14px rgba(75, 65, 225, 0.3));
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(75, 65, 225, 0.4);
  background: var(--app-btn-primary-bg-hover, linear-gradient(135deg, #645bf7 0%, #4338ca 100%));
}

.af-btn-black {
  background: var(--app-slate-900, #0f172a);
  color: var(--app-on-primary, #ffffff);
  border: 1px solid rgba(255, 255, 255, 0.1);
  height: var(--app-btn-primary-height, 42px);
  padding: 0 1.25rem;
  border-radius: var(--app-btn-radius-md, 0.75rem);
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-btn-black:hover {
  transform: translateY(-1px);
  background: var(--app-slate-800, #1e293b);
  box-shadow: 0 6px 16px rgba(15, 23, 42, 0.25);
}

.af-btn-outline {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(203, 213, 225, 0.8);
  color: var(--app-slate-700, #334155);
  height: var(--app-btn-primary-height, 42px);
  padding: 0 1.1rem;
  border-radius: var(--app-btn-radius-md, 0.75rem);
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  backdrop-filter: blur(4px);
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-btn-outline:hover {
  background: #ffffff;
  border-color: var(--app-slate-400, #94a3b8);
  color: var(--app-slate-900, #0f172a);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
</style>