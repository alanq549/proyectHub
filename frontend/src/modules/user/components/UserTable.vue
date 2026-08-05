<template>
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0 custom-glass-table">
      <thead>
        <tr>
          <th class="ps-4" style="width: 70px;">ID</th>
          <th>Usuario / Info</th>
          <th>Correo Electrónico</th>
          <th>Rol</th>
          <th>Estado</th>
          <th class="text-end pe-4">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td class="ps-4 fw-semibold text-muted">#{{ user.id }}</td>
          <td>
            <div class="d-flex align-items-center gap-3">
              <img
                :src="getUserAvatar(user)"
                alt="Avatar"
                class="rounded-circle object-fit-cover user-avatar"
                width="40"
                height="40"
              />
              <div>
                <div class="fw-bold text-dark mb-0 user-name">
                  {{ getFullName(user) }}
                </div>
                <span class="text-muted small">@{{ user.username }}</span>
              </div>
            </div>
          </td>
          <td class="text-secondary small fw-medium">{{ user.email }}</td>
          <td>
            <span
              class="badge-pill"
              :class="user.role === 'admin' ? 'badge-admin' : 'badge-user'"
            >
              <span class="material-symbols-outlined notranslate fs-6">
                {{ user.role === 'admin' ? 'admin_panel_settings' : 'person' }}
              </span>
              <span>{{ user.role === 'admin' ? 'Administrador' : 'Usuario' }}</span>
            </span>
          </td>
          <td>
            <span
              class="badge-pill"
              :class="user.is_active !== false ? 'badge-active' : 'badge-inactive'"
            >
              <span class="status-dot"></span>
              <span>{{ user.is_active !== false ? 'Activo' : 'Inactivo' }}</span>
            </span>
          </td>
          <td class="text-end pe-4">
            <div class="d-inline-flex gap-1">
              <button
                class="btn-action"
                title="Editar usuario"
                @click="$emit('edit', user)"
              >
                <span class="material-symbols-outlined notranslate fs-5">edit</span>
              </button>
              <button
                class="btn-action btn-action-danger"
                title="Eliminar usuario"
                @click="$emit('delete', user.id!)"
              >
                <span class="material-symbols-outlined notranslate fs-5">delete</span>
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="users.length === 0">
          <td colspan="6" class="text-center py-5 text-muted">
            <span class="material-symbols-outlined notranslate fs-1 text-secondary mb-2">group_off</span>
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
  --bs-table-bg: transparent;
  --bs-table-hover-bg: rgba(15, 23, 42, 0.03);
  margin-bottom: 0;
}

.custom-glass-table thead {
  background: rgba(15, 23, 42, 0.03);
  border-bottom: 1px solid var(--app-slate-200);
}

.custom-glass-table thead th {
  color: var(--app-slate-500);
  font-size: 0.725rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding-top: 1rem;
  padding-bottom: 1rem;
  border-bottom: none;
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