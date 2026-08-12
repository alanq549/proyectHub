<template>
  <!--
    DashboardHeroCard — Bloque 1.2 (Migración Bootstrap → Tailwind)
    • Clase glassmorphism .app-card-glass-xl GLOBAL de main.css intacta (transición).
    • Utilidades Bootstrap (text-start / d-flex / mt-* / align-items-*) migradas a *.
    • Botones mantienen clases locales af-btn-* (son estilos custom, no Bootstrap).
    • Paleta "PROJECTHUB" navy + dorado, coherente con Login/Register/CallCard.
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
        <button class="af-btn-primary" @click="$emit('primary-action')">
          <span class="material-symbols-outlined notranslate" style="font-size: 18px;">manage_accounts</span>
          {{ primaryActionLabel }}
        </button>
        <button class="af-btn-outline" @click="$emit('secondary-action')">
          <span class="material-symbols-outlined notranslate" style="font-size: 18px;">download</span>
          {{ secondaryActionLabel }}
        </button>
        <button v-if="showCreateAction" class="af-btn-black" @click="$emit('create-action')">
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
  primaryActionLabel: string
  secondaryActionLabel: string
  showCreateAction?: boolean
}>()

defineEmits<{
  (event: 'primary-action'): void
  (event: 'secondary-action'): void
  (event: 'create-action'): void
}>()
</script>

<style scoped>
.material-symbols-outlined { vertical-align: middle; font-family: 'Material Symbols Outlined' !important; }
.notranslate { -webkit-translate: no; translate: no; }

/* ============================================================
   Paleta "PROJECTHUB" — navy #10192B + dorado #C9974A
   Se apoya en las variables globales --ph-navy / --ph-gold ya
   definidas en :root (ver Login.vue / Register.vue).
   ============================================================ */

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
    rgba(247, 245, 238, 0.75) 60%,
    rgba(238, 227, 205, 0.55) 100%
  );
}

/* Destello sutil de fondo, ahora en tono dorado */
.af-hero-glow {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(201, 151, 74, 0.18) 0%, rgba(255, 255, 255, 0) 70%);
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

/* Anillo del avatar en degradé navy → dorado */
.af-avatar-wrapper {
  position: relative;
  border-radius: 50%;
  padding: 3px;
  background: linear-gradient(135deg, var(--ph-navy, #10192B) 0%, var(--ph-gold, #C9974A) 100%);
  box-shadow: 0 4px 12px rgba(16, 25, 43, 0.15);
}

.af-hero-title {
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
  font-size: 26px;
  font-weight: 700;
  color: var(--ph-navy, #10192B);
  margin: 0;
  letter-spacing: -0.01em;
}

/* Badges con diseño neumórfico/soft */
.af-role-badge {
  background: var(--ph-gold-soft, rgba(201, 151, 74, 0.12));
  color: var(--ph-gold, #C9974A);
  border: 1px solid rgba(201, 151, 74, 0.3);
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

/* Estilos de Botones — navy como color primario de marca */
.af-btn-primary {
  background: linear-gradient(135deg, var(--ph-navy, #10192B) 0%, var(--ph-navy-soft, #16233b) 100%);
  color: #ffffff;
  border: none;
  height: var(--app-btn-primary-height, 42px);
  padding: 0 1.25rem;
  border-radius: var(--app-btn-radius-md, 0.75rem);
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  box-shadow: 0 4px 14px rgba(16, 25, 43, 0.3);
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(16, 25, 43, 0.4);
  background: linear-gradient(135deg, #16233b 0%, #0c1420 100%);
}

/* Botón "Nueva Auditoría" en dorado, como CTA de acento */
.af-btn-black {
  background: var(--ph-gold, #C9974A);
  color: var(--ph-navy, #10192B);
  border: 1px solid rgba(16, 25, 43, 0.08);
  height: var(--app-btn-primary-height, 42px);
  padding: 0 1.25rem;
  border-radius: var(--app-btn-radius-md, 0.75rem);
  font-size: 14px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  box-shadow: 0 4px 12px rgba(201, 151, 74, 0.3);
  transition: all 0.2s ease;
  cursor: pointer;
}

.af-btn-black:hover {
  transform: translateY(-1px);
  background: #d9ab5e;
  box-shadow: 0 6px 16px rgba(201, 151, 74, 0.4);
}

.af-btn-outline {
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(203, 213, 225, 0.8);
  color: var(--ph-navy, #10192B);
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
  border-color: var(--ph-navy, #10192B);
  color: var(--ph-navy, #10192B);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 25, 43, 0.08);
}
</style>
