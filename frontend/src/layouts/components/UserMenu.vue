<!-- src/layouts/components/UserMenu.vue -->
<template>
    <AppDropdown align="end" v-model="open">
        <template #trigger="{ open, toggle }">
            <button
                class="avatar-btn"
                type="button"
                :aria-expanded="open"
                aria-haspopup="true"
                @click.stop="toggle"
            >
                <UserAvatar :src="user.avatarUrl" :alt="`Perfil ${user.name}`" size="sm" />
            </button>
        </template>

        <!-- Cabecera de usuario -->
        <div class="user-info-header tw-px-3 tw-py-2 tw-mb-1">
            <div class="tw-font-semibold tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-xs" style="max-width:160px;">
                {{ user.name }}
            </div>
            <div class="tw-text-slate-500 tw-lowercase tw-text-xs" style="font-size:.75rem;">
                {{ user.email }}
            </div>
        </div>

        <!-- Opción: Perfil -->
        <button
            type="button"
            class="app-dropdown-item tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-2 tw-text-slate-900 tw-text-sm tw-w-full tw-text-left"
            @click="goToProfile"
        >
            <span class="material-symbols-outlined notranslate tw-text-lg">person</span>
            <span>Perfil</span>
        </button>

        <!-- Separador -->
        <div class="dropdown-divider tw-my-1"></div>

        <!-- Opción: Cerrar Sesión -->
        <button
            type="button"
            class="app-dropdown-item item-logout tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-2 tw-text-sm tw-w-full tw-text-left"
            @click="$emit('logout')"
        >
            <span class="material-symbols-outlined notranslate tw-text-lg">logout</span>
            <span>Cerrar sesión</span>
        </button>
    </AppDropdown>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import UserAvatar from './UserAvatar.vue';
import AppDropdown from '@/shared/components/AppDropdown.vue';

interface User {
    name: string
    email?: string
    avatarUrl: string
}

defineProps<{
    user: User
}>()

defineEmits<{
    logout: []
}>()

const open = ref(false);
const router = useRouter();

const goToProfile = () => {
    open.value = false;
    router.push({ name: 'user-profile' });
};
</script>

<style scoped>
/* Reset absoluto anti-Bootstrap */
.avatar-btn,
.app-dropdown-item {
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    appearance: none !important;
    -webkit-appearance: none !important;
}

.avatar-btn {
    padding: 0;
    cursor: pointer;
    display: inline-flex;
}

.user-info-header {
    border-bottom: 1px solid var(--app-slate-200, #e2e8f0) !important;
}

.dropdown-divider {
    height: 1px;
    background-color: var(--app-slate-200, #e2e8f0);
}

.app-dropdown-item {
    transition: background-color 0.12s ease;
    cursor: pointer;
    border-radius: 0.375rem;
}

.app-dropdown-item:hover {
    background-color: var(--app-slate-100, #f1f5f9) !important;
}

.app-dropdown-item.item-logout {
    color: var(--app-error, #ba1a1a);
}

.app-dropdown-item.item-logout:hover {
    background-color: var(--app-error-bg, rgba(254, 226, 226, 0.8)) !important;
}
</style>