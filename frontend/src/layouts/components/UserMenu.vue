<template>
    <AppDropdown align="end" v-model="open">
        <template #trigger="{ open, toggle }">
            <button
                class="avatar-btn border-0 bg-transparent p-0 cursor-pointer outline-none inline-flex"
                type="button"
                :aria-expanded="open"
                aria-haspopup="true"
                @click.stop="toggle"
            >
                <UserAvatar :src="user.avatarUrl" :alt="`Perfil ${user.name}`" size="sm" />
            </button>
        </template>

        <div class="px-3 py-2 border-b border-slate-100 mb-1">
            <div class="font-semibold overflow-hidden text-ellipsis whitespace-nowrap text-xs" style="max-width:160px;">
                {{ user.name }}
            </div>
            <div class="text-slate-500 lowercase text-xs" style="font-size:.75rem;">
                {{ user.email }}
            </div>
        </div>

        <button
            class="app-dropdown-item flex items-center gap-2 px-3 py-2 text-slate-900 hover:bg-slate-100 text-base w-full text-left"
            @click="goToProfile"
        >
            <span class="material-symbols-outlined notranslate text-xl">person</span>
            <span>Perfil</span>
        </button>

        <hr class="my-1 border-slate-100" />

        <button
            class="app-dropdown-item text-error flex items-center gap-2 px-3 py-2 hover:bg-error/10 text-base w-full text-left"
            @click="$emit('logout')"
        >
            <span class="material-symbols-outlined notranslate text-xl">logout</span>
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
.avatar-btn {
    cursor: pointer;
    outline: none;
}
.app-dropdown-item {
    transition: background-color 0.12s ease;
    cursor: pointer;
}
</style>