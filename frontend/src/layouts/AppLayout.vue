<template>
    <div class="dashboard-root">
        <!-- Top Navbar -->
        <header class="topbar">
            <div class="d-flex align-items-center gap-3">
                <span class="material-symbols-outlined notranslate"
                    style="font-variation-settings: 'FILL' 1;">account_tree</span>
                <span class="brand-name notranslate">ProjectHub</span>
            </div>
            <div class="d-flex align-items-center gap-1">
                <button class="icon-btn" @click="searchOpen = true">
                    <span class="material-symbols-outlined notranslate">search</span>
                </button>
                <button class="icon-btn position-relative">
                    <span class="material-symbols-outlined notranslate">notifications</span>
                    <span class="notif-dot"></span>
                </button>
                <div class="avatar-sm">
                    <img :src="authStore.avatarUrl" :alt="`Perfil ${authStore.user?.username}`" />
                </div>
            </div>

            <div class="search-overlay" :class="{ open: searchOpen }">
                <span class="material-symbols-outlined notranslate" style="color: var(--outline);">search</span>
                <input v-model="searchQuery" type="text" placeholder="Buscar proyectos, recursos..."
                    ref="searchInput" />
                <button class="search-close-btn notranslate" @click="searchOpen = false">Cerrar</button>
            </div>
        </header>

        <!-- Rail Navigation -->
        <aside class="rail-nav">
            <a v-for="item in railItems" :key="item.icon" href="#" class="rail-link"
                :class="{ active: activeRail === item.key }" @click.prevent="navigateRail(item)">
                <span class="material-symbols-outlined notranslate"
                    :style="activeRail === item.key ? { fontVariationSettings: `'FILL' 1` } : {}">{{ item.icon }}</span>
            </a>
            <a href="#" class="rail-link mt-auto" :class="{ active: activeRail === 'settings' }"
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
            <button v-for="item in bottomNavItems.slice(0, 2)" :key="item.key" class="bnav-item"
                :class="{ active: activeBottomNav === item.key }" @click="navigateBottomNav(item)">
                <span class="material-symbols-outlined notranslate"
                    :style="activeBottomNav === item.key ? { fontVariationSettings: `'FILL' 1` } : {}">{{ item.icon
                    }}</span>
                <span class="lbl">{{ item.label }}</span>
            </button>

            <button class="bnav-fab" @click="$emit('new-project')">
                <span class="material-symbols-outlined notranslate fs-4">add</span>
            </button>

            <button v-for="item in bottomNavItems.slice(2)" :key="item.key" class="bnav-item"
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


const VITE_STATIC_URL = import.meta.env.VITE_STATIC_URL
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

// ==============================
// Tipos
// ==============================

interface RailItem {
    key: string
    icon: string
    routeName?: string
}

interface BottomNavItem {
    key: string
    icon: string
    label: string
    routeName?: string
}

interface UserDisplay {
    name: string
    role: string
    avatarUrl: string
}

// ==============================
// Mapeos de Navegación (key → route.name)
// ==============================

const ROUTE_NAME_BY_KEY: Record<string, string> = {
    dashboard: 'dashboard',
    research: 'dashboard',
    calendar: 'dashboard',
    documents: 'users-list',
    settings: 'dashboard',
    home: 'dashboard',
    explore: 'dashboard',
    inbox: 'dashboard',
    profile: 'users-list',
    admin_users: 'users-list',
}

// ==============================
// Elementos de Navegación
// ==============================

const railItems: RailItem[] = [
    { key: 'dashboard', icon: 'dashboard', routeName: 'dashboard' },
    { key: 'research', icon: 'folder_open', routeName: 'dashboard' },
    { key: 'calendar', icon: 'analytics', routeName: 'dashboard' },
    { key: 'documents', icon: 'group', routeName: 'users-list' },
]

const bottomNavItems: BottomNavItem[] = [
    { key: 'home', icon: 'home', label: 'Inicio', routeName: 'dashboard' },
    { key: 'explore', icon: 'explore', label: 'Explorar', routeName: 'dashboard' },
    { key: 'inbox', icon: 'mail', label: 'Inbox', routeName: 'dashboard' },
    { key: 'profile', icon: 'person', label: 'Perfil', routeName: 'users-list' },
]

// ==============================
// Estado Activo (sincronizado con vue-router)
// ==============================

const activeRail = computed<string>(() => {
    const currentName = String(route.name ?? '')
    const matched = railItems.find((it) => it.routeName === currentName)
    if (matched) return matched.key
    if (currentName === '') return 'dashboard'
    // settings si no coincide nada
    return 'dashboard'
})

const activeBottomNav = computed<string>(() => {
    const currentName = String(route.name ?? '')
    const matched = bottomNavItems.find((it) => it.routeName === currentName)
    return matched?.key ?? 'home'
})

// ==============================
// Acciones de Navegación
// ==============================

function navigateRail(item: RailItem): void {
    const target = item.routeName ?? ROUTE_NAME_BY_KEY[item.key] ?? 'dashboard'
    if (route.name !== target) {
        router.push({ name: target }).catch(() => undefined)
    }
}

function navigateBottomNav(item: BottomNavItem): void {
    const target = item.routeName ?? ROUTE_NAME_BY_KEY[item.key] ?? 'dashboard'
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

// ==============================
// Emits
// ==============================

defineEmits<{
    (event: 'new-project'): void
    (event: 'upload-file'): void
}>()
</script>

<style scoped>
:root,
.dashboard-root {
    --primary: #000000;
    --on-primary-container: #7c839b;
    --background: #f7f9fb;
    --tertiary-fixed: #acedff;
    --on-tertiary-container: #0090a9;
    --surface-container-lowest: #ffffff;
    --on-surface-variant: #45464d;
    --surface-container-low: #f2f4f6;
    --secondary-fixed: #e2dfff;
    --on-primary: #ffffff;
    --secondary: #4b41e1;
    --outline-variant: #c6c6cd;
    --outline: #76777d;
    --error: #ba1a1a;
    --on-surface: #191c1e;
    --surface-container: #eceef0;
    --surface-container-high: #e6e8ea;
    --secondary-container: #645efb;
}

.dashboard-root {
    font-family: 'Inter', sans-serif;
    background-color: var(--background);
    color: var(--on-surface);
    overflow-x: hidden;
    position: relative;
    min-height: 100vh;
}

.material-symbols-outlined {
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    font-family: 'Material Symbols Outlined' !important;
    font-style: normal;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-smoothing: antialiased;
    font-synthesis: none;
    text-rendering: optimizeLegibility;
    vertical-align: middle;
}

.notranslate {
    -webkit-translate: no;
    translate: no;
}

.glass {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(226, 232, 240, 0.5);
}

.scrollbar-hide::-webkit-scrollbar {
    display: none;
}

.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}

/* Top navbar */
.topbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1050;
    height: 64px;
    background-color: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
}

.logo-box {
    width: 32px;
    height: 32px;
    background-color: var(--primary);
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 700;
    font-size: 20px;
}

.brand-name {
    font-weight: 700;
    font-size: 20px;
    color: var(--primary);
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
    background-color: var(--surface-container-high);
}

.icon-btn .material-symbols-outlined {
    color: var(--on-surface-variant);
}

.notif-dot {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    background-color: var(--error);
    border-radius: 50%;
    border: 2px solid #fff;
}

.avatar-sm {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: #e0e3e5;
    overflow: hidden;
    margin-left: 0.25rem;
}

.avatar-sm img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.search-overlay {
    position: absolute;
    inset: 0;
    background: #fff;
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
}

.search-overlay input:focus {
    outline: none;
    box-shadow: none;
}

.search-close-btn {
    background: none;
    border: none;
    color: var(--secondary);
    font-size: 14px;
    font-weight: 500;
    padding: 0.5rem;
}

/* Rail nav */
.rail-nav {
    position: fixed;
    left: 0;
    top: 64px;
    bottom: 0;
    width: 64px;
    background-color: var(--surface-container-low);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0;
    gap: 24px;
    z-index: 1040;
    border-right: 1px solid rgba(198, 198, 205, 0.3);
}

.rail-link {
    padding: 12px;
    border-radius: 0.75rem;
    color: var(--on-surface-variant);
    transition: background-color .2s ease;
    text-decoration: none;
}

.rail-link:hover {
    background-color: var(--surface-container-high);
}

.rail-link.active {
    color: var(--secondary);
    background-color: rgba(75, 65, 225, 0.08);
}

/* Main content */
.main-content {
    padding-top: 80px;
    padding-left: calc(64px + 16px);
    padding-right: 16px;
    padding-bottom: 96px;
    min-height: 100vh;
}

/* Bottom nav */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
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
    color: var(--on-surface-variant);
}

.bnav-item.active {
    color: var(--primary);
}

.bnav-item .lbl {
    font-size: 10px;
    font-weight: 600;
}

.bnav-fab {
    width: 56px;
    height: 56px;
    background-color: var(--secondary);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    border: none;
    box-shadow: 0 10px 15px -3px rgba(75, 65, 225, 0.3);
    position: relative;
    top: -16px;
    transition: transform .1s ease;
}

.bnav-fab:active {
    transform: scale(0.9);
}

.fs-4 {
    font-size: 24px;
}

/* Background effect */
.bg-effect {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: -1;
    opacity: 0.30;
}

.bg-blob-1 {
    position: absolute;
    top: 25%;
    right: -10%;
    width: 300px;
    height: 300px;
    background-color: var(--secondary);
    border-radius: 50%;
    filter: blur(120px);
}

.bg-blob-2 {
    position: absolute;
    bottom: 25%;
    left: -10%;
    width: 300px;
    height: 300px;
    background-color: var(--tertiary-fixed);
    border-radius: 50%;
    filter: blur(120px);
}
</style>
