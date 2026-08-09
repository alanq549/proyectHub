<!--src/layouts/AppLayout.vue -->
<template>
    <div class="dashboard-root">
        <!-- Top Navbar -->
        <header class="topbar">
            <div class="tw-flex tw-items-center tw-gap-3">
                <span class="material-symbols-outlined notranslate"
                    style="font-variation-settings: 'FILL' 1;">account_tree</span>
                <span class="brand-name notranslate">ProjectHub</span>
            </div>
            <div class="tw-flex tw-items-center tw-gap-1">
                <button class="icon-btn" @click="searchOpen = true">
                    <span class="material-symbols-outlined notranslate">search</span>
                </button>
                <button class="icon-btn tw-relative">
                    <span class="material-symbols-outlined notranslate">notifications</span>
                    <span class="notif-dot"></span>
                </button>

                <!-- User Dropdown Menu nativo via AppDropdown -->
                <AppDropdown align="end" v-model="userMenuOpen">
                    <template #trigger="{ open, toggle }">
                        <button
                            class="avatar-btn tw-border-0 tw-bg-transparent tw-p-0 tw-cursor-pointer tw-outline-none tw-ml-1"
                            type="button" :aria-expanded="open" aria-haspopup="true" @click.stop="toggle">
                            <div class="avatar-sm">
                                <img :src="authStore.avatarUrl" :alt="`Perfil ${authStore.user?.username}`" />
                            </div>
                        </button>
                    </template>

                    <div class="tw-px-3 tw-py-2 tw-border-b tw-border-slate-100 tw-mb-1">
                        <div class="tw-font-semibold tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-xs"
                            style="max-width: 160px;">
                            {{ user.name }}
                        </div>
                        <div class="tw-text-slate-500 tw-lowercase tw-text-xs" style="font-size: 0.75rem;">
                            {{ authStore.user?.email }}
                        </div>
                    </div>

                    <button
                        class="app-dropdown-item tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-2 tw-text-base tw-w-full tw-text-left tw-border-0 tw-bg-transparent hover:tw-bg-slate-100 tw-text-slate-900"
                        @click="handleNavigateProfile">
                        <span class="material-symbols-outlined notranslate tw-text-xl">person</span>
                        <span>Perfil</span>
                    </button>

                    <hr class="tw-my-1 tw-border-slate-100" />

                    <button
                        class="app-dropdown-item tw-text-red-600 tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-2 tw-text-base tw-w-full tw-text-left tw-border-0 tw-bg-transparent hover:tw-bg-red-50 tw-rounded-md"
                        @click="handleLogout">
                        <span class="material-symbols-outlined notranslate tw-text-xl">logout</span>
                        <span>Cerrar sesión</span>
                    </button>
                </AppDropdown>
            </div>

            <div class="search-overlay" :class="{ open: searchOpen }">
                <span class="material-symbols-outlined notranslate" style="color: var(--outline);">search</span>
                <input v-model="searchQuery" type="text" placeholder="Buscar proyectos, recursos..."
                    ref="searchInput" />
                <button class="search-close-btn notranslate" @click="searchOpen = false">Cerrar</button>
            </div>
        </header>

        <!-- Punto 3.3 & 3.4: Rail Navigation con filtrado por rol -->
        <aside class="rail-nav">
            <template v-for="item in visibleRailItems" :key="item.key">
                <a href="#" class="rail-link" :class="{ active: activeRail === item.key }" :title="item.title"
                    @click.prevent="navigateRail(item)">
                    <span class="material-symbols-outlined notranslate"
                        :style="activeRail === item.key ? { fontVariationSettings: `'FILL' 1` } : {}">{{ item.icon
                        }}</span>
                </a>
            </template>
            <a href="#" class="rail-link mt-auto" title="Configuración" :class="{ active: activeRail === 'settings' }"
                @click.prevent="navigateRail({ key: 'settings', icon: 'settings' })">
                <span class="material-symbols-outlined notranslate">settings</span>
            </a>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <RouterView />
        </main>

        <!-- Bottom Navigation (Mobile) -->
        <nav class="bottom-nav">
            <button v-for="item in visibleBottomNavItems.slice(0, 2)" :key="item.key" class="bnav-item"
                :class="{ active: activeBottomNav === item.key }" @click="navigateBottomNav(item)">
                <span class="material-symbols-outlined notranslate"
                    :style="activeBottomNav === item.key ? { fontVariationSettings: `'FILL' 1` } : {}">{{ item.icon
                    }}</span>
                <span class="lbl">{{ item.label }}</span>
            </button>

            <button class="bnav-fab" @click="$emit('new-project')">
                <span class="material-symbols-outlined notranslate tw-text-2xl">add</span>
            </button>

            <button v-for="item in visibleBottomNavItems.slice(2)" :key="item.key" class="bnav-item"
                :class="{ active: activeBottomNav === item.key }" @click="navigateBottomNav(item)">
                <span class="material-symbols-outlined notranslate"
                    :style="activeBottomNav === item.key ? { fontVariationSettings: `'FILL' 1` } : {}">{{ item.icon
                    }}</span>
                <span class="lbl">{{ item.label }}</span>
            </button>
        </nav>

        <!-- Background effect -->
        <div class="bg-effect">
            <div class="bg-blob-1"></div>
            <div class="bg-blob-2"></div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import AppDropdown from '@/shared/components/AppDropdown.vue'

const VITE_STATIC_URL = import.meta.env.VITE_STATIC_URL
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const userMenuOpen = ref(false)

// ==============================
// Tipos
// ==============================

interface RailItem {
    key: string
    icon: string
    title: string
    routeName?: string
    adminOnly?: boolean
}

interface BottomNavItem {
    key: string
    icon: string
    label: string
    routeName?: string
    adminOnly?: boolean
}

interface UserDisplay {
    name: string
    role: string
    avatarUrl: string
}

// ==============================
// Acciones de Dropdown
// ==============================

function handleNavigateProfile(): void {
    userMenuOpen.value = false
    router.push({ name: 'user-profile' })
}

function handleLogout(): void {
    userMenuOpen.value = false
    authStore.logout()
    router.push({ name: 'login' })
}

// ==============================
// Elementos de Navegación (Puntos 3.3 & 3.4)
// ==============================

const railItems: RailItem[] = [
    { key: 'dashboard', icon: 'dashboard', title: 'Dashboard', routeName: 'dashboard' },
    { key: 'users', icon: 'group', title: 'Usuarios', routeName: 'users-list', adminOnly: true },
    { key: 'calls', icon: 'campaign', title: 'Convocatorias', routeName: 'calls-list' },
    { key: 'projects', icon: 'folder', title: 'Mis proyectos', routeName: 'projects-list' },
    { key: 'documents', icon: 'description', title: 'Mis documentos', routeName: 'documents-list' },
    { key: 'history', icon: 'history', title: 'Historial', routeName: 'history' },
]

const bottomNavItems: BottomNavItem[] = [
    { key: 'home', icon: 'home', label: 'Inicio', routeName: 'dashboard' },
    { key: 'users', icon: 'group', label: 'Usuarios', routeName: 'users-list', adminOnly: true },
    { key: 'projects', icon: 'folder', label: 'Mis proyectos', routeName: 'projects-list' },
    { key: 'history', icon: 'history', label: 'Historial', routeName: 'history' },
]

// Filtrar ítems visibles según rol
const visibleRailItems = computed(() => {
    return railItems.filter((item) => !item.adminOnly || authStore.isAdmin)
})

const visibleBottomNavItems = computed(() => {
    return bottomNavItems.filter((item) => !item.adminOnly || authStore.isAdmin)
})

// ==============================
// Estado Activo (sincronizado con vue-router)
// ==============================

const activeRail = computed<string>(() => {
    const currentName = String(route.name ?? '')
    const matched = visibleRailItems.value.find((it) => it.routeName === currentName)
    return matched ? matched.key : 'dashboard'
})

const activeBottomNav = computed<string>(() => {
    const currentName = String(route.name ?? '')
    const matched = visibleBottomNavItems.value.find((it) => it.routeName === currentName)
    return matched ? matched.key : 'home'
})

// ==============================
// Acciones de Navegación
// ==============================

function navigateRail(item: Partial<RailItem>): void {
    const target = item.routeName ?? 'dashboard'
    if (route.name !== target) {
        router.push({ name: target }).catch(() => undefined)
    }
}

function navigateBottomNav(item: BottomNavItem): void {
    const target = item.routeName ?? 'dashboard'
    if (route.name !== target) {
        router.push({ name: target }).catch(() => undefined)
    }
}

// ==============================
// Búsqueda expandible
// ==============================

const searchOpen = ref<boolean>(false)
const searchQuery = ref<string>('')
const searchInput = ref<HTMLInputElement | null>(null)

watch(searchOpen, async (open: boolean) => {
    if (open) {
        await nextTick()
        searchInput.value?.focus()
    }
})

// ==============================
// Usuario (conectado al authStore)
// ==============================

const DEFAULT_AVATAR = `${VITE_STATIC_URL}/static/defaults/icon_default.png`

const ROLE_LABELS: Record<'admin' | 'user', string> = {
    admin: 'Administrador',
    user: 'Usuario',
}

function buildDisplayName(): string {
    const u = authStore.user
    if (!u) return 'Usuario'
    const parts: string[] = []
    if (u.first_name) parts.push(u.first_name)
    if (u.last_name) parts.push(u.last_name)
    if (parts.length > 0) return parts.join(' ')
    return u.username
}

function buildRoleLabel(): string {
    const u = authStore.user
    if (!u) return 'Usuario'
    return ROLE_LABELS[u.role] ?? u.role
}

const user = computed<UserDisplay>(() => ({
    name: buildDisplayName(),
    role: buildRoleLabel(),
    avatarUrl: authStore.user?.profile_picture_url || DEFAULT_AVATAR,
}))

defineEmits<{
    (event: 'new-project'): void
    (event: 'upload-file'): void
}>()
</script>

<style scoped>
.dashboard-root {
    background-color: var(--app-bg-main, #f1f5f9);
    background-image: var(--app-bg-gradient);
    background-attachment: fixed;
    /* Evita que el degradado se corte al hacer scroll */
    color: var(--app-on-surface, #0f172a);
    overflow-x: hidden;
    position: relative;
    min-height: 100vh;
}

.avatar-btn {
    cursor: pointer;
    outline: none;
}

.app-dropdown-item {
    cursor: pointer;
    transition: background-color 0.12s ease;
}

.app-dropdown-item:active {
    background-color: var(--app-surface-container-high, #e6e8ea);
    color: var(--app-on-surface, #191c1e);
}

/* Top navbar — Ahora consume tokens globales --app-topbar-* */
.topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1050;
    height: 64px;
    background-color: var(--app-topbar-bg, rgba(255, 255, 255, 0.82));
    backdrop-filter: var(--app-glass-blur, blur(16px));
    -webkit-backdrop-filter: var(--app-glass-blur, blur(16px));
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
}

.brand-name {
    font-weight: 700;
    font-size: 20px;
    color: var(--app-black, #000);
}

.icon-btn {
    padding: 0.5rem;
    border: none;
    background: none;
    border-radius: 50%;
    transition: background-color .15s ease;
    position: relative;
}

.icon-btn:hover {
    background-color: var(--app-surface-container-high, #e6e8ea);
}

.icon-btn .material-symbols-outlined {
    color: var(--app-on-surface-variant, #45464d);
}

.notif-dot {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    background-color: var(--app-error, #ba1a1a);
    border-radius: 50%;
    border: 2px solid #fff;
}

.avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: var(--app-surface-container-highest, #e0e3e5);
    overflow: hidden;
}

.avatar-sm img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.search-overlay {
    position: absolute;
    inset: 0;
    background: var(--app-surface-container-lowest, #fff);
    z-index: 1060;
    display: flex;
    align-items: center;
    padding: 0 16px;
    gap: 0.75rem;
    transform: translateY(-100%);
    transition: transform .3s ease;
}

.search-overlay.open {
    transform: translateY(0);
}

.search-overlay input {
    flex: 1;
    background: transparent;
    border: none;
    font-size: 16px;
    padding: 0.5rem 0;
    color: var(--app-on-surface, #191c1e);
}

.search-overlay input:focus {
    outline: none;
    box-shadow: none;
}

.search-close-btn {
    background: none;
    border: none;
    color: var(--app-primary, #4b41e1);
    font-size: 14px;
    font-weight: 500;
    padding: 0.5rem;
}

/* Rail nav — Ahora consume tokens globales */
.rail-nav {
    position: fixed;
    left: 0;
    top: 64px;
    bottom: 0;
    width: 64px;
    background-color: var(--app-rail-bg, var(--app-surface-container-low, #f2f4f6));
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0;
    gap: 24px;
    z-index: 1040;
    border-right: var(--app-rail-border, 1px solid rgba(198, 198, 205, 0.3));
}

.rail-link {
    padding: 12px;
    border-radius: var(--app-glass-radius-sm, 0.75rem);
    color: var(--app-on-surface-variant, #45464d);
    transition: background-color .2s ease;
    text-decoration: none;
}

.rail-link:hover {
    background-color: var(--app-surface-container-high, #e6e8ea);
}

.rail-link.active {
    color: var(--app-primary, #4b41e1);
    background-color: rgba(75, 65, 225, 0.08);
}

/* Main content */
.main-content {
    position: relative;
    z-index: 1;
    padding-top: 80px;
    padding-left: calc(64px + 16px);
    padding-right: 16px;
    padding-bottom: 96px;
    min-height: 100vh;
}

/* Rail oculto en Mobile (<768px) */
@media (max-width: 767.98px) {
    .rail-nav {
        display: none;
    }

    .main-content {
        padding-left: 16px;
    }
}

/* Bottom nav — Consume tokens globales --app-bottomnav-* */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: var(--app-bottomnav-bg, rgba(255, 255, 255, 0.90));
    backdrop-filter: var(--app-glass-blur-sm, blur(12px));
    -webkit-backdrop-filter: var(--app-glass-blur-sm, blur(12px));
    border-top: 1px solid rgba(198, 198, 205, 0.2);
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 0 16px;
    z-index: 1050;
}

@media (min-width: 768px) {
    .bottom-nav {
        display: none;
    }
}

.bnav-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    background: none;
    border: none;
    color: var(--app-on-surface-variant, #45464d);
}

.bnav-item.active {
    color: var(--app-black, #000);
}

.bnav-item .lbl {
    font-size: 10px;
    font-weight: 600;
}

.bnav-fab {
    width: 56px;
    height: 56px;
    background-color: var(--app-primary, #4b41e1);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--app-on-primary, #fff);
    border: none;
    box-shadow: var(--app-btn-primary-shadow, 0 10px 15px -3px rgba(75, 65, 225, 0.3));
    position: relative;
    top: -16px;
    transition: transform .1s ease;
}

.bnav-fab:active {
    transform: scale(0.9);
}

/* Background effect — Blobs consumen tokens --app-bg-blob-* para fácilmente cambiables */
.bg-effect {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    /* Queda justo sobre el fondo del layout, pero debajo del contenido */
    opacity: var(--app-bg-blob-opacity, 0.85);
}



.bg-blob-1 {
    position: absolute;
    top: 25%;
    right: -10%;
    width: 300px;
    height: 300px;
    background-color: var(--app-bg-blob-primary, rgba(75, 65, 225, 0.25));
    border-radius: 50%;
    filter: var(--app-bg-blob-blur, blur(120px));
}

.bg-blob-2 {
    position: absolute;
    bottom: 25%;
    left: -10%;
    width: 300px;
    height: 300px;
    background-color: var(--app-bg-blob-secondary, rgba(172, 237, 255, 0.30));
    border-radius: 50%;
    filter: var(--app-bg-blob-blur, blur(120px));
}
</style>
