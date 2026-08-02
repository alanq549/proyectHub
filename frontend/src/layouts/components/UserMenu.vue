<template>
    <div class="dropdown ms-1">
        <button class="avatar-btn dropdown-toggle border-0 bg-transparent p-0" type="button" data-bs-toggle="dropdown"
            aria-expanded="false">
                <UserAvatar :src="user.avatarUrl" :alt="`Perfil ${user.name}`" size="sm" />
        </button>


        <ul class="dropdown-menu dropdown-menu-end shadow-sm rounded-3 py-2 border-0">

            <li class="px-3 py-2 border-bottom mb-1">
                <div class="fw-semibold text-truncate small" style="max-width:160px;">
                    {{ user.name }}
                </div>

                <div class="text-muted text-lowercase small" style="font-size:.75rem;">
                    {{ user.email }}
                </div>
            </li>


            <li>
                <button class="dropdown-item d-flex align-items-center gap-2 py-2 fs-6" @click="$emit('profile')">
                    <span class="material-symbols-outlined notranslate fs-5">
                        person
                    </span>

                    <span>
                        Perfil
                    </span>
                </button>
            </li>


            <li>
                <hr class="dropdown-divider">
            </li>


            <li>
                <button class="dropdown-item text-danger d-flex align-items-center gap-2 py-2 fs-6"
                    @click="$emit('logout')">
                    <span class="material-symbols-outlined notranslate fs-5">
                        logout
                    </span>

                    <span>
                        Cerrar sesión
                    </span>
                </button>
            </li>

        </ul>
    </div>
</template>


<script setup lang="ts">
import UserAvatar from './UserAvatar.vue';

interface User {
    name: string
    email?: string
    avatarUrl: string
}


defineProps<{
    user: User
}>()


defineEmits<{
    profile: []
    logout: []
}>()

</script>

<style scoped>

.avatar-btn::after {
    display: none;
}

.avatar-btn {
    cursor: pointer;
    outline: none;
}

</style>