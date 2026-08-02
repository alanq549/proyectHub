<template>
  <section class="af-hero-card">
    <div class="af-hero-banner d-flex justify-content-center align-items-center"></div>
    <div class="af-hero-body">
      <div class="af-hero-left">
        <UserAvatar 
  :src="user.avatarUrl"
  :alt="`Perfil ${user.name}`"
  size="lg"
/>
        <div class="mb-2">
          <h2 class="af-hero-title notranslate">¡Hola de nuevo, {{ user.name }}! 👋</h2>
          <div class="d-flex align-items-center justify-content-center justify-content-md-start gap-3 mt-1">
            <span class="af-hero-subtitle">{{ user.role }}</span>
            <span class="af-secure-badge">
              <span class="material-symbols-outlined notranslate" style="font-size:14px;">lock</span>
              Conexión Segura
            </span>
          </div>
        </div>
      </div>
      <div class="d-flex gap-3 mb-2">
        <button class="af-btn-outline" @click="$emit('download-report')">Descargar Reporte</button>
        <button class="af-btn-black" @click="$emit('new-audit')">
          Nueva Auditoría
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import UserAvatar from '@/layouts/components/UserAvatar.vue'


export interface DashboardHeroUser {
  name: string
  role: string
  avatarUrl: string
}


const props = defineProps<{
  user: DashboardHeroUser
}>()


console.log('DashboardHeroCard user:', props.user)


defineEmits<{
  (event: 'download-report'): void
  (event: 'new-audit'): void
}>()

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

.af-btn-black {
  background: #000;
  color: #fff;
  border: none;
  height: 42px;
  padding: 0 1.25rem;
  border-radius: 0.75rem;
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: .5rem;
  cursor: pointer;
  transition: all .2s ease;

}

.af-btn-black:hover {
  background: #45464d;
}

.af-btn-black:active {
  transform: scale(.98);
}

.af-hero-card {
  margin-bottom: 48px;
  position: relative;
  border-radius: 1.25rem;
  overflow: hidden;

  /* Mezcla de gradiente horizontal primario + fundido vertical hacia blanco en la base */
  background:
    linear-gradient(to top, var(--af-surface-container-lowest, #ffffff) 0%, transparent 60%),
    linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, var(--af-surface-container-low, #f2f4f6) 100%);


  border: 1px solid rgba(0, 0, 0, .08);

  box-shadow:
    0 1px 2px rgba(0, 0, 0, .04),
    0 12px 32px rgba(0, 0, 0, .08);
}

.af-hero-banner {
  height: 128px;
  width: 100%;
  background: linear-gradient(to right, rgba(19, 27, 46, 0.6), transparent);
}

.af-hero-body {
  padding: 0 32px 32px;
  margin-top: -40px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .af-hero-body {
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }
}

.af-hero-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
}

@media (min-width: 768px) {
  .af-hero-left {
    flex-direction: row;
    align-items: flex-end;
    text-align: left;
  }
}

.af-avatar-96 {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 4px solid var(--af-surface, #f7f9fb);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  background: #fff;
}

.af-avatar-96 img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.af-hero-title {
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--af-primary, #000);
  margin: 0;
}

.af-hero-subtitle {
  font-size: 14px;
  color: var(--af-on-surface-variant, #45464d);
}

.af-secure-badge {
  padding: 0.25rem 0.75rem;
  background-color: #dcfce7;
  color: #166534;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 9999px;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  border: 1px solid #bbf7d0;
}

.af-btn-outline {
  background-color: #fff;
  border: 1px solid var(--af-outline-variant, #c6c6cd);
  color: var(--af-primary, #000);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 14px;
  transition: background-color .15s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.af-btn-outline:hover {
  background-color: var(--af-surface-container-low, #f2f4f6);
}

.af-btn-secondary {
  background-color: var(--af-secondary, #4b41e1);
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 14px;
  transition: opacity .15s ease;
  box-shadow: 0 10px 15px -3px rgba(75, 65, 225, 0.2);
}

.af-btn-secondary:hover {
  opacity: 0.9;
  color: #fff;
}
</style>
