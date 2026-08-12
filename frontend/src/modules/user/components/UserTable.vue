<template>
  <div class="tw-overflow-x-auto">
    <table class="tw-w-full tw-align-middle">
      <thead class="tw-bg-surface-container-low/50 tw-border-b tw-border-outline-variant">
        <tr>
          <th class="tw-ps-4 tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider" style="width: 70px;">ID</th>
          <th class="tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider">Usuario / Info</th>
          <th class="tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider">Correo Electrónico</th>
          <th class="tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider">Rol</th>
          <th class="tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider">Estado</th>
          <th class="tw-text-right tw-pe-4 tw-py-4 tw-text-xs tw-font-bold tw-text-on-surface-variant tw-uppercase tw-tracking-wider">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="user in users"
          :key="user.id"
          class="tw-border-b tw-border-black/[0.04] hover:tw-bg-surface-container-low/30 tw-transition-colors"
        >
          <td class="tw-ps-4 tw-py-3 tw-font-semibold tw-text-on-surface-variant">#{{ user.id }}</td>
          <td class="tw-py-3">
            <div class="tw-flex tw-items-center tw-gap-3">
              <img
                :src="getUserAvatar(user)"
                alt="Avatar"
                class="tw-rounded-full tw-object-cover tw-border tw-border-outline-variant tw-shadow-sm"
                width="40"
                height="40"
              />
              <div>
                <div class="tw-font-bold tw-text-on-surface tw-text-sm">{{ getFullName(user) }}</div>
                <span class="tw-text-on-surface-variant tw-text-xs">@{{ user.username }}</span>
              </div>
            </div>
          </td>
          <td class="tw-py-3 tw-text-on-surface-variant tw-text-xs tw-font-medium">{{ user.email }}</td>
          <td class="tw-py-3">
            <AppBadge :variant="user.role === 'admin' ? 'primary' : 'neutral'" :icon="user.role === 'admin' ? 'admin_panel_settings' : 'person'">
              {{ user.role === 'admin' ? 'Administrador' : 'Usuario' }}
            </AppBadge>
          </td>
          <td class="tw-py-3">
            <AppBadge :variant="user.is_active !== false ? 'success' : 'error'" :dot="true">
              {{ user.is_active !== false ? 'Activo' : 'Inactivo' }}
            </AppBadge>
          </td>
          <td class="tw-text-right tw-pe-4 tw-py-3">
            <div class="tw-inline-flex tw-gap-1">
              <AppButton variant="ghost" size="sm" icon="edit" @click="$emit('edit', user)" />
              <AppButton variant="danger" size="sm" icon="delete" @click="$emit('delete', user.id!)" />
            </div>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="6" class="tw-text-center tw-py-10 tw-text-on-surface-variant">
            <span class="material-symbols-outlined notranslate tw-text-4xl tw-text-outline tw-block tw-mb-2">group_off</span>
            <p class="tw-text-sm">No se encontraron usuarios con los criterios seleccionados.</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { User } from '../services/userService';
import AppBadge from '@/shared/components/AppBadge.vue';
import AppButton from '@/shared/components/AppButton.vue';

defineProps<{
  users: User[];
}>();

defineEmits<{
  (e: 'edit', user: User): void;
  (e: 'delete', id: number): void;
}>();

const defaultAvatar = '/static/defaults/icon_default.png';

const getUserAvatar = (user: User) => {
  if (!user.profile_picture_url) {
    return defaultAvatar;
  }

  if (user.profile_picture_url.startsWith('/')) {
    return user.profile_picture_url;
  }

  return user.profile_picture_url;
};

const getFullName = (user: User) => {
  const name = [user.first_name, user.last_name].filter(Boolean).join(' ');
  return name.length > 0 ? name : user.username;
};
</script>