<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { userService } from '../services/userService';
import UserAvatar from '@/layouts/components/UserAvatar.vue';

const authStore = useAuthStore();

const profileForm = reactive({
    first_name: '',
    last_name: '',
    username: '',
    email: ''
});

const passwordForm = reactive({
    current_password: '',
    new_password: '',
    confirm_password: ''
});

const selectedFile = ref<File | null>(null);
const previewUrl = ref<string | null>(null);

const profileMessage = ref({ type: '', text: '' });
const passwordMessage = ref({ type: '', text: '' });
const isSavingProfile = ref(false);
const isSavingPassword = ref(false);

onMounted(() => {
    if (authStore.user) {
        profileForm.first_name = authStore.user.first_name || '';
        profileForm.last_name = authStore.user.last_name || '';
        profileForm.username = authStore.user.username || '';
        profileForm.email = authStore.user.email || '';
    }
});

const handleFileChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        const file = target.files[0];
        selectedFile.value = file;
        previewUrl.value = URL.createObjectURL(file);
    }
};

const handleUpdateProfile = async () => {
    if (!authStore.user?.id) return;
    isSavingProfile.value = true;
    profileMessage.value = { type: '', text: '' };

    try {
        const formData = new FormData();
        formData.append('first_name', profileForm.first_name);
        formData.append('last_name', profileForm.last_name);
        formData.append('username', profileForm.username);
        formData.append('email', profileForm.email);

        if (selectedFile.value) {
            formData.append('file', selectedFile.value);
        }

        const updatedUser = await userService.updateUser(authStore.user.id, formData);
        authStore.updateUserData(updatedUser.user || updatedUser);

        profileMessage.value = { type: 'success', text: 'Perfil actualizado correctamente.' };
    } catch (error: any) {
        profileMessage.value = {
            type: 'error',
            text: error.response?.data?.error || 'Error al actualizar el perfil.'
        };
    } finally {
        isSavingProfile.value = false;
    }
};

const handleChangePassword = async () => {
    passwordMessage.value = { type: '', text: '' };

    if (passwordForm.new_password !== passwordForm.confirm_password) {
        passwordMessage.value = { type: 'error', text: 'Las nuevas contraseñas no coinciden.' };
        return;
    }

    if (passwordForm.new_password.length < 6) {
        passwordMessage.value = { type: 'error', text: 'La contraseña debe tener al menos 6 caracteres.' };
        return;
    }

    isSavingPassword.value = true;

    try {
        await userService.changePassword({
            current_password: passwordForm.current_password,
            new_password: passwordForm.new_password
        });

        passwordMessage.value = { type: 'success', text: 'Contraseña actualizada con éxito.' };
        passwordForm.current_password = '';
        passwordForm.new_password = '';
        passwordForm.confirm_password = '';
    } catch (error: any) {
        passwordMessage.value = {
            type: 'error',
            text: error.response?.data?.error || 'Error al cambiar la contraseña.'
        };
    } finally {
        isSavingPassword.value = false;
    }
};
</script>

<template>
    <div class="container py-4 max-w-profile">
        <!-- Header Principal de la Página -->
        <div class="d-flex align-items-center gap-3 mb-4">
            <div class="header-icon-box rounded-3 d-flex align-items-center justify-content-center p-2">
                <span class="material-symbols-outlined notranslate fs-2">manage_accounts</span>
            </div>
            <div>
                <h1 class="h3 fw-bold text-dark mb-0">Configuración de Perfil</h1>
                <p class="text-muted small mb-0">Administra tus datos personales y credenciales de acceso a la plataforma.</p>
            </div>
        </div>

        <!-- Sección 1: Información Personal -->
        <div class="card glass-card border-0 shadow-sm rounded-4 mb-4">
            <div class="card-body p-4">
                <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
                    <span class="material-symbols-outlined text-primary notranslate">person_gear</span>
                    <h2 class="h5 fw-semibold mb-0">Información Personal</h2>
                </div>

                <!-- Banner de Alertas -->
                <div v-if="profileMessage.text"
                    :class="`alert alert-${profileMessage.type === 'success' ? 'success' : 'danger'} alert-dismissible fade show d-flex align-items-center gap-2 py-2 px-3 small rounded-3`"
                    role="alert">
                    <span class="material-symbols-outlined notranslate fs-5">
                        {{ profileMessage.type === 'success' ? 'check_circle' : 'error' }}
                    </span>
                    <div>{{ profileMessage.text }}</div>
                </div>

                <form @submit.prevent="handleUpdateProfile">
                    <!-- Área de Carga de Avatar -->
                    <div class="profile-avatar-wrapper d-flex align-items-center gap-4 mb-4 p-3 rounded-3 bg-light-subtle">
                        <div class="position-relative">
                            <UserAvatar :src="previewUrl || authStore.avatarUrl" :alt="profileForm.username" size="lg" />
                            <div class="avatar-badge rounded-circle bg-primary text-white d-flex align-items-center justify-content-center">
                                <span class="material-symbols-outlined notranslate fs-6">photo_camera</span>
                            </div>
                        </div>
                        <div class="flex-grow-1">
                            <label for="avatarInput" class="form-label fw-medium small mb-1 d-flex align-items-center gap-1">
                                <span class="material-symbols-outlined notranslate fs-6 text-muted">image</span>
                                Foto de perfil
                            </label>
                            <input id="avatarInput" type="file" @change="handleFileChange" accept="image/*" class="form-control form-control-sm" />
                            <div class="form-text small opacity-75 d-flex align-items-center gap-1 mt-1">
                                <span class="material-symbols-outlined notranslate fs-6">info</span>
                                Formatos recomendados: JPG, PNG. Tamaño máx: 2MB
                            </div>
                        </div>
                    </div>

                    <!-- Campos del Formulario de Perfil con Iconos Integrados -->
                    <div class="row g-3">
                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Nombre</label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">badge</span>
                                </span>
                                <input v-model="profileForm.first_name" type="text" class="form-control app-input-control" placeholder="Tu nombre" />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Apellido</label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">badge</span>
                                </span>
                                <input v-model="profileForm.last_name" type="text" class="form-control app-input-control" placeholder="Tu apellido" />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Nombre de Usuario <span class="text-danger">*</span></label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">alternate_email</span>
                                </span>
                                <input v-model="profileForm.username" type="text" required class="form-control app-input-control" placeholder="username" />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Correo Electrónico <span class="text-danger">*</span></label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">mail</span>
                                </span>
                                <input v-model="profileForm.email" type="email" required class="form-control app-input-control" placeholder="correo@ejemplo.com" />
                            </div>
                        </div>
                    </div>

                    <div class="d-flex justify-content-end pt-4">
                        <button :disabled="isSavingProfile" type="submit" class="btn btn-primary d-inline-flex align-items-center gap-2 px-4 py-2 rounded-3 fw-medium">
                            <span v-if="isSavingProfile" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            <span class="material-symbols-outlined notranslate fs-5" v-else>save</span>
                            <span>{{ isSavingProfile ? 'Guardando...' : 'Guardar Cambios' }}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Sección 2: Seguridad y Contraseña -->
        <div class="card glass-card border-0 shadow-sm rounded-4">
            <div class="card-body p-4">
                <div class="d-flex align-items-center gap-2 mb-4 pb-2 border-bottom">
                    <span class="material-symbols-outlined text-primary notranslate">shield</span>
                    <h2 class="h5 fw-semibold mb-0">Seguridad & Contraseña</h2>
                </div>

                <!-- Banner de Alertas de Contraseña -->
                <div v-if="passwordMessage.text"
                    :class="`alert alert-${passwordMessage.type === 'success' ? 'success' : 'danger'} alert-dismissible fade show d-flex align-items-center gap-2 py-2 px-3 small rounded-3`"
                    role="alert">
                    <span class="material-symbols-outlined notranslate fs-5">
                        {{ passwordMessage.type === 'success' ? 'check_circle' : 'error' }}
                    </span>
                    <div>{{ passwordMessage.text }}</div>
                </div>

                <form @submit.prevent="handleChangePassword">
                    <div class="row g-3">
                        <div class="col-12">
                            <label class="form-label fw-medium small">Contraseña Actual <span class="text-danger">*</span></label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">lock</span>
                                </span>
                                <input v-model="passwordForm.current_password" type="password" required class="form-control app-input-control" placeholder="••••••••" />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Nueva Contraseña <span class="text-danger">*</span></label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">password</span>
                                </span>
                                <input v-model="passwordForm.new_password" type="password" required class="form-control app-input-control" placeholder="Mínimo 6 caracteres" />
                            </div>
                        </div>

                        <div class="col-md-6">
                            <label class="form-label fw-medium small">Confirmar Nueva Contraseña <span class="text-danger">*</span></label>
                            <div class="input-group app-input-group">
                                <span class="input-group-text app-input-group-text">
                                    <span class="material-symbols-outlined notranslate fs-5">enhanced_encryption</span>
                                </span>
                                <input v-model="passwordForm.confirm_password" type="password" required class="form-control app-input-control" placeholder="Repite la contraseña" />
                            </div>
                        </div>
                    </div>

                    <div class="d-flex justify-content-end pt-4">
                        <button :disabled="isSavingPassword" type="submit" class="btn btn-dark d-inline-flex align-items-center gap-2 px-4 py-2 rounded-3 fw-medium">
                            <span v-if="isSavingPassword" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            <span class="material-symbols-outlined notranslate fs-5" v-else>vpn_key</span>
                            <span>{{ isSavingPassword ? 'Actualizando...' : 'Actualizar Contraseña' }}</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.max-w-profile {
    max-width: 860px;
}

.header-icon-box {
    background: rgba(99, 102, 241, 0.1);
    color: var(--app-primary, #6366f1);
}

/*
  IMPORTANTE: Ya NO re-declaramos .glass-card aquí.
  La clase viene del sistema UNIFICADO en main.css:219-226 con
  tokens --app-glass-* consistentes con todo el resto del dashboard.
  El template sigue usando class="card glass-card" que apunta a la
  regla GLOBAL, no a una scoped con borde diferente.
*/

.profile-avatar-wrapper {
    border: 1px dashed rgba(0, 0, 0, 0.12);
}

.avatar-badge {
    position: absolute;
    bottom: -2px;
    right: -2px;
    width: 24px;
    height: 24px;
    border: 2px solid var(--app-surface-container-lowest, #ffffff);
}

/*
  Inputs: Ahora el template usa clases GLOBALES
  .app-input-group / .app-input-group-text / .app-input-control
  definidas en main.css. Las reglas scoped de aquí ya no son necesarias
  para bordes / focus / radius / padding — las hereda del sistema.
  Se deja este bloque vacío intencionalmente para futuros overrides
  específicos del perfil (si los hubiera).
*/
</style>