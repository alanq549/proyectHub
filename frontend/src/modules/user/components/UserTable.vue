<template>
  <div class="overflow-x-auto">
    <table class="w-full align-middle mb-0 custom-glass-table">
      <thead>
        <tr>
          <th class="ps-4 text-xs font-bold text-slate-500 uppercase tracking-wider" style="width: 70px;">ID</th>
          <th class="text-xs font-bold text-slate-500 uppercase tracking-wider">Usuario / Info</th>
          <th class="text-xs font-bold text-slate-500 uppercase tracking-wider">Correo Electrónico</th>
          <th class="text-xs font-bold text-slate-500 uppercase tracking-wider">Rol</th>
          <th class="text-xs font-bold text-slate-500 uppercase tracking-wider">Estado</th>
          <th class="text-right pe-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id" class="hover:bg-slate-50/50">
          <td class="ps-4 font-semibold text-slate-500">#{{ user.id }}</td>
          <td class="py-3">
            <div class="flex items-center gap-3">
              <img
                :src="getUserAvatar(user)"
                alt="Avatar"
                class="rounded-pill object-cover user-avatar"
                width="40"
                height="40"
              />
              <div>
                <div class="font-bold text-slate-900 mb-0 user-name">
                  {{ getFullName(user) }}
                </div>
                <span class="text-slate-500 text-xs">@{{ user.username }}</span>
              </div>
            </div>
          </td>
          <td class="text-slate-500 text-xs font-medium">{{ user.email }}</td>
          <td class="py-3">
            <span
              class="badge-pill"
              :class="user.role === 'admin' ? 'badge-admin' : 'badge-user'"
            >
              <span class="material-symbols-outlined notranslate text-base">
                {{ user.role === 'admin' ? 'admin_panel_settings' : 'person' }}
              </span>
              <span>{{ user.role === 'admin' ? 'Administrador' : 'Usuario' }}</span>
            </span>
          </td>
          <td class="py-3">
            <span
              class="badge-pill"
              :class="user.is_active !== false ? 'badge-active' : 'badge-inactive'"
            >
              <span class="status-dot"></span>
              <span>{{ user.is_active !== false ? 'Activo' : 'Inactivo' }}</span>
            </span>
          </td>
          <td class="text-right pe-4">
            <div class="inline-flex gap-1">
              <button
                class="btn-action"
                title="Editar usuario"
                @click="$emit('edit', user)"
              >
                <span class="material-symbols-outlined notranslate text-lg">edit</span>
              </button>
              <button
                class="btn-action btn-action-danger"
                title="Eliminar usuario"
                @click="$emit('delete', user.id!)"
              >
                <span class="material-symbols-outlined notranslate text-lg">delete</span>
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="6" class="text-center py-5 text-slate-500">
            <span class="material-symbols-outlined notranslate text-4xl text-slate-500 mb-2">group_off</span>
            <p class="mb-0">No se encontraron usuarios con los criterios seleccionados.</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { User } from '../services/userService';

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
    return `http://127.0.0.1:5000${user.profile_picture_url}`;
  }
  return user.profile_picture_url;
};

const getFullName = (user: User) => {
  const name = [user.first_name, user.last_name].filter(Boolean).join(' ');
  return name.length > 0 ? name : user.username;
};
</script>

<style scoped>
.custom-glass-table {
  background: transparent;
  margin-bottom: 0;
  border-collapse: separate;
  border-spacing: 0;
}

.custom-glass-table thead {
  background: rgba(15, 23, 42, 0.03);
  border-bottom: 1px solid var(--app-slate-200);
}

.custom-glass-table thead th {
  color: var(--app-slate-500);
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-bottom: none;
  border-collapse: separate;
}

.custom-glass-table tbody td {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.custom-glass-table tbody tr {
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  transition: background-color 0.2s ease;
}

.user-avatar {
  border: 1px solid var(--app-slate-200);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.user-name {
  color: var(--app-slate-900);
  font-size: 0.925rem;
}

/* Insignias Personalizadas */
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.65rem;
  border-radius: var(--app-radius-pill);
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-admin {
  background: var(--app-slate-900);
  color: #ffffff;
}

.badge-user {
  background: var(--app-slate-100);
  color: var(--app-slate-700);
  border: 1px solid var(--app-slate-200);
}

.badge-active {
  background: var(--app-success-bg);
  color: var(--app-success);
}

.badge-inactive {
  background: var(--app-error-bg);
  color: var(--app-error);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

/* Botones de acción minimalistas */
.btn-action {
  width: 32px;
  height: 32px;
  border-radius: 0.5rem;
  border: 1px solid transparent;
  background: transparent;
  color: var(--app-slate-600);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background: #ffffff;
  border-color: var(--app-slate-200);
  color: var(--app-slate-900);
  box-shadow: 0 2px 4px rgba(0,0,0,0.04);
}

.btn-action-danger:hover {
  background: var(--app-error-bg);
  border-color: rgba(186, 26, 26, 0.2);
  color: var(--app-error);
}
</style>