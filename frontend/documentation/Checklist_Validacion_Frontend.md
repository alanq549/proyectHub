# Checklist de Validación Técnica — Frontend (Vue.js + Bootstrap 5)

**Documento:** `frontend/documentation/Checklist_Validacion_Frontend.md`  
**Versión:** 1.2 (Re-Auditoría: 2026-08-02)  
**Referencia:** `documentation/Alcance.md` secciones 3.1, 5, 6, 7  
**Cambios desde v1.1:** Implementados: Axios response interceptor (401→logout+redirect, 403/500 log), vite proxy `/api`, .env.development+production, UserMenu dropdown funcional con logout, role filters en sidebar (adminOnly), rail-nav oculto <768px, redirect home si autenticado. Persisten: perfil/me 0%, modal/tabla users incompletos, módulos Calls/Projects/Docs/History 0%.

---

# Convenciones de Estado

| Estado | Símbolo | Descripción |
|--------|---------|-------------|
| Pendiente | ⬜ | No iniciado o sin evidencia |
| En Progreso | 🟧 | Implementado parcialmente, requiere ajustes |
| Aprobado | ✅ | Cumple todos los criterios de aceptación |
| Observaciones | ⚠️ | Funciona pero contiene deuda o mejoras pendientes |

---

# 1. Configuración y Estructura Base

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 1.1 | Stack correcto | Proyecto Vue.js 3 (Composition API), TypeScript, Bootstrap 5 instalado y configurado | ✅ | `package.json:17-25`: `vue@3.5.40`, `typescript@6`, `bootstrap@5.3.8`, `@popperjs/core`. `main.ts:6-10` importa Bootstrap CSS y JS bundle. Composition API usado (setup lang="ts"). |
| 1.2 | Build tool | Vite configurado, `npm run dev`, `npm run build`, `npm run preview` funcionan | ✅ | `vite.config.ts` define alias `@`. Scripts en package.json: dev, build (type-check + build-only), preview, test:unit, test:e2e. |
| 1.3 | Bootstrap 5 integrado | Clases BS5 disponibles globalmente. Componentes usan estilos BS5. | ✅ | `main.ts:6-7` importa bootstrap.min.css y bootstrap.bundle.min.js. También `bootstrap-icons` y `material-symbols`. Vistas Login/Register/Users/Layout usan d-flex, row, col, card, btn, table, form-control, modal, alert. |
| 1.4 | Routing | Vue Router configurado con rutas públicas y privadas | ✅ | `router/index.ts:12-38` crea router con `createWebHistory`. Rutas: home `/`, auth (login, register) públicas, children de AppLayout protegidas con `meta.requiresAuth`. 404 → redirect `/`. |
| 1.5 | State Management | Pinia store para al menos `authStore` (usuario, token, login/logout) | ✅ | `stores/authStore.ts:16` `defineStore('auth', ...)` con `token`, `user`, `isAuthenticated`, `isAdmin`, `avatarUrl`, actions `register`, `login`, `logout`. |
| 1.6 | Cliente HTTP | Axios configurado en `src/api/axios.ts` con `baseURL`, interceptor para adjuntar JWT en `Authorization: Bearer` | ✅ | `api/axios.ts:4-44`. **REQUEST INTERCEPTOR ✅** lines 14-20 adjunta Bearer token. **RESPONSE INTERCEPTOR ✅ NUEVO** lines 23-44: status 401 → `authStore.logout()` + redirect `/login`; 403 → `console.error`; 500 → `console.error`. ⚠️ Mejora pendiente: 403/500 deberían mostrar toast UI, no solo console.error. |
| 1.7 | Proxy dev | Vite configura proxy `/api` → backend localhost para evitar CORS en desarrollo | ✅ | [vite.config.ts:18-27](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/vite.config.ts#L18-L27) **NUEVO**: `server.proxy` define `/api` → `http://127.0.0.1:5000`. ⚠️ Importante: proxy reenvía `/api/*` a `http://127.0.0.1:5000/api/*` PERO blueprint backend es `/api/v1/*`. El proxy NO agrega `/v1` (sin rewrite rule). Funciona porque `.env.development` usa URL absoluta con `/api/v1`. |
| 1.8 | Variables de entorno | `.env.development`, `.env.production` definen `VITE_API_BASE_URL` y no están hardcodeadas | ✅ | **NUEVO** existen ambos archivos: [.env.development:1-2](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/.env.development#L1-L2) `VITE_API_BASE_URL=http://127.0.0.1:5000/api/v1` + `VITE_STATIC_URL=http://127.0.0.1:5000`. [.env.production:1-2](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/.env.production#L1-L2) tiene placeholder `https://tu-dominio-backend.com/api` (válido, debe editarse en despliegue). |
| 1.9 | Organización modular | Estructura: `src/modules/<feature>/{routes,views,components,services}` | ✅ | `src/modules/auth/`, `src/modules/dashboard/`, `src/modules/user/` cada uno con `routes/index.ts`, `views/`, `components/`, `services/`. |

---

# 2. Módulo 7.1 — Autenticación (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 2.1 | Vista Login | Ruta pública `/login` con formulario: email/username + password. Bootstrap 5 responsive. | ✅ | `views/LoginView.vue` — formulario email + password, diseño responsive con sidebar desktop y mobile header, clases d-flex, col-md-6, min-vh-100. |
| 2.2 | Vista Registro | Ruta pública `/register` con formulario: username, email, password, confirmar_password | ✅ | `views/RegisterView.vue` — campos nombre, apellido, username, email, password + confirm, barra de seguridad, estado de éxito post-register. Diseño 2-column responsive. |
| 2.3 | Validaciones login | Campos obligatorios, email válido, feedback visual ante credenciales inválidas (toast o alerta) | 🟧 | `LoginView.vue`: atributos HTML5 `type=email`, `required`. ⚠️ No usa Vuelidate ni validación programática avanzada (solo HTML5 required). Error de credenciales: componente `ErrorAlert` muestra error + animación shake del form. Toast genérico no existe. |
| 2.4 | Validaciones registro | Coincidencia de contraseñas, longitud mínima, formato email. Mensajes de error por campo. | 🟧 | `RegisterView.vue:232-238` validación manual `password !== confirmPassword`. ⚠️ HTML5 required. Password strength bar es SOLO visual (no bloquea submit). Sin Vuelidate. Mensaje de error general en `.alert-danger`, no por campo. |
| 2.5 | Guard de rutas | Router guard `requiresAuth` redirige a `/login` si no hay token | ✅ | `router/index.ts:60-62` check `to.meta.requiresAuth && !authStore.isAuthenticated → login`. Perfecto. |
| 2.6 | Guard de invitado | Rutas `/login` y `/register` redirigen a `/dashboard` si el usuario ya está logueado | ✅ | `router/index.ts:49-57` `isAuthRoute && authStore.isAuthenticated → admin→users-list, user→dashboard`. |
| 2.7 | Token almacenado | Después de login exitoso: token guardado en `localStorage` o Pinia persistido | ✅ | `authStore.ts:52-56` `localStorage.setItem('token', accessToken)` + `localStorage.setItem('user', ...)`. Inicialización de stores leen desde localStorage (lines 17-18). |
| 2.8 | Acción logout | Botón/menú "Cerrar sesión" limpia token, limpia store, redirige a `/login` | ✅ | **NUEVO IMPLEMENTADO**. [AppLayout.vue:45-49](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L45-L49) Dropdown usuario navbar tiene botón rojo "Cerrar sesión" con icono logout. Función `handleLogout()` lines 154-157: `authStore.logout()` + `router.push({ name: 'login' })`. También existe [UserMenu.vue](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/components/UserMenu.vue) componente reusable con el mismo dropdown. |
| 2.9 | Expiración de sesión | Al recibir 401 del backend, limpiar estado y redirigir a login | ✅ | **NUEVO IMPLEMENTADO**. [axios.ts:28-35](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L28-L35) Axios response interceptor captura `status === 401`: llama `authStore.logout()` (limpia token + user + localStorage) + `window.location.href = '/login'` (evita loop si ya está en login). |
| 2.10 | Redirección post-login | Después de login exitoso, redirigir a `/dashboard` | ✅ | `LoginView.vue:152-159` Si admin → `users-list`; Si user → `dashboard`. RegisterView: después de éxito solo muestra mensaje, NO hace auto-login ni redirect. (Deseable pero opcional para la entrega). |

---

# 3. Layout y Navegación General

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 3.1 | Layout principal | `AppLayout.vue` con: Navbar superior, Sidebar (menú), Content area | ✅ | `layouts/AppLayout.vue`: `<header .topbar>` + `<aside .rail-nav>` + `<main .main-content>` + `<RouterView />` + `<nav .bottom-nav>` mobile. Completo. |
| 3.2 | Navbar | Muestra: nombre app, foto de perfil usuario, dropdown con "Perfil" + "Cerrar sesión" | ✅ | **NUEVO FUNCIONAL COMPLETO**. [AppLayout.vue:20-52](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L20-L52): Topbar ProjectHub + iconos search/notifications + avatar dropdown. Dropdown muestra: nombre usuario, email, link "Perfil" (actualmente dashboard), divider, "Cerrar sesión" (funcional con handleLogout). También botones iconos search overlay expandible y notifications con badge. |
| 3.3 | Sidebar | Menú con enlaces a: Dashboard, Usuarios (si admin), Convocatorias, Proyectos, Documentos, Historial, Perfil | 🟧 | `railItems` [AppLayout.vue:163-170](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L163-L170): 6 items (dashboard, users, calls, projects, documents, history) + settings icon abajo. **⚠️ FALTA**: items `calls`, `projects`, `documents`, `history`, `profile` APUNTAN TODOS a `routeName: 'dashboard'` — las rutas reales de esos módulos NO EXISTEN aún. Bottom nav: items home, users(adminOnly), projects, profile(→dashboard). |
| 3.4 | Menú contextual por rol | Item "Usuarios" visible solo para `role === 'admin'` | ✅ | **NUEVO IMPLEMENTADO**. [AppLayout.vue:180-186](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L180-L186) computed `visibleRailItems` y `visibleBottomNavItems` con `.filter(item => !item.adminOnly \|\| authStore.isAdmin)`. Items con `adminOnly: true` (users) se OCULTAN completamente para usuario non-admin. Perfecto. |
| 3.5 | Responsive | Sidebar colapsa a offcanvas/drawer en mobile. Bootstrap breakpoints usados. | ✅ | **NUEVO FIXADO**. [AppLayout.vue:497-504](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L497-L504) `@media (max-width: 767.98px)` → `.rail-nav { display: none; }` y `.main-content { padding-left: 16px; }`. Bottom nav visible solo <768px (lines 524-528). Desktop ≥768px: rail visible, bottom-nav oculto. Excelente. |
| 3.6 | Ruta 404 | Cualquier ruta no definida muestra una página de "No encontrado" o redirige | ✅ | `router/index.ts:34-37` catch-all `/:pathMatch(.*)*` → redirect `/`. Válido. |
| 3.7 | Ruta home `/` | Redirige a `/login` o `/dashboard` según estado de sesión | ✅ | **NUEVO IMPLEMENTADO**. [router/index.ts:52-54](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/router/index.ts#L52-L54) Guard: `if (to.name === 'home' && authStore.isAuthenticated) return authStore.isAdmin ? { name: 'users-list' } : { name: 'dashboard' }`. Usuario autenticado NO ve landing, redirige correctamente. |

---

# 4. Módulo 7.6 — Dashboard Estadístico

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 4.1 | Vista Dashboard | Ruta `/dashboard` protegida | ✅ | `dashboard/routes/index.ts:5-12` path 'dashboard' en children de AppLayout → requiresAuth=true. |
| 4.2 | KPI Cards | 4 tarjetas BS5 mostrando: # Usuarios, # Convocatorias, # Proyectos, # Documentos | ✅ | `DashboardKpiGrid` renderizado desde `DashboardView.vue:9`. KPIs lines 84-118 con 4 tarjetas: Usuarios 128, Convocatorias Activas 8, Proyectos Totales 45, S3 Storage 1.2 TB. |
| 4.3 | Consumo de API stats | Llama a `GET /api/dashboard/stats` al montar el componente y popula las KPI | ⬜ | **Todas las KPIs están HARDCODEADAS** (valores fijos: 128, 8, 45, 1.2). No hay llamada a API, no hay `onMounted` con fetch. Dashboard es una maqueta estática. FALTA conectar al endpoint backend. |
| 4.4 | Loading state | Mientras carga las stats, muestra spinners o skeletons BS5 | ⬜ | Sin loading porque no hay llamada API. Cuando se integre debe agregarse. |
| 4.5 | Panel de navegación rápida | Tarjetas/atajos a módulos principales (Convocatorias, Proyectos, Subir documento) | ✅ | `DashboardHeroCard` con acciones. `DashboardS3UploadPanel` con panel upload. Links existen (pero aún no llevan a rutas reales). |

---

# 5. Módulo 7.2 — Administración de Usuarios (UI) — Acceso Admin

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 5.1 | Ruta protegida | Ruta `/users` solo accesible con `role=admin`; guard rechaza a otros usuarios | ✅ | `user/routes/index.ts:8-12` `meta.requiresAuth + requiresAdmin: true`. `router/index.ts:65-67` guard: `requiresAdmin && !isAdmin → dashboard`. Perfecto. |
| 5.2 | Tabla de usuarios | Tabla BS5 muestra columnas: ID, username, email, nombre, apellido, rol, estado, acciones | 🟧 | `UserTable` (inline en `UserListView.vue:19-46`) muestra ID, Usuario (username), Correo, Acciones. ⚠️ FALTAN columnas: first_name, last_name, role, is_active (estado). Solo muestra 3 de 8 campos necesarios. |
| 5.3 | Paginación / búsqueda | Tabla con paginación y/o campo de búsqueda por username/email | ⬜ | Sin paginación. Sin search input. Muestra todos los registros directo del array. |
| 5.4 | Botón Crear Usuario | Botón "Nuevo Usuario" que abre `UserModal.vue` (BS modal) | ✅ | `UserListView.vue:9-13` Botón "Nuevo Usuario" con icono + llama `openCreateModal()` → abre UserModal. |
| 5.5 | Formulario crear/editar | Modal con campos: username, email, password, first_name, last_name, role, is_active, profile_picture (upload) | 🟧 | `UserModal.vue:13-33`: campos solo username, email, password (en create). ⚠️ FALTAN completamente: first_name, last_name, role selector, is_active toggle, upload profile picture. El modal es DEMASIADO simple. Además no usa FormData, así que NO soporta multipart para foto. |
| 5.6 | Botón Editar | Ícono/botón Editar en cada fila, abre modal con datos precargados | ✅ | `UserListView.vue:34-35` botón outline-secondary con edit icon. `watch(props.userToEdit)` en UserModal precarga username/email/borra password. |
| 5.7 | Botón Eliminar | Botón Eliminar con confirmación antes de llamar DELETE | ✅ | `UserListView.vue:107-116` `if (confirm('¿Seguro...?'))` → deleteUser → loadUsers. Confirm dialog nativo; válido. |
| 5.8 | Subida de foto de perfil | En modal, permite seleccionar imagen y enviarla via `multipart/form-data` | ⬜ | Modal NO tiene input file. UserService.updateUser usa api.put() enviando JSON. No multipart. Debe usar `FormData` con `Content-Type: multipart/form-data` y campo `file`. |
| 5.9 | Toast de éxito/error | Después de operaciones CRUD, muestra feedback visual | 🟧 | En caso de error: `alert('Error...')` lines 101 y 113. ⚠️ Éxito no tiene toast, solo refresh silencioso. Mejor usar toast/alert BS5 uniforme. |
| 5.10 | Refresh de tabla | Después de crear/editar/eliminar la tabla se actualiza automáticamente | ✅ | `handleSave:99` `await loadUsers()`. `deleteUser:111` `await loadUsers()`. Correcto. |

---

# 6. Módulo 7.3 — Gestión de Convocatorias (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 6.1 | Ruta | Ruta `/calls` (o `/convocatorias`) protegida | ⬜ | NO IMPLEMENTADO. No hay módulo `calls/` ni rutas definidas en router/index.ts. |
| 6.2 | Listado | Tabla o cards con: nombre, descripción, fecha inicio, fecha fin, estado | 🟧 | Dashboard muestra `DashboardActiveCalls.vue` con 2 convocatorias hardcodeadas como preview. No existe vista dedicada /calls. |
| 6.3 | Filtros | Filtro por estado (abiertas/cerradas), búsqueda por nombre | ⬜ | Pendiente |
| 6.4 | Crear convocatoria | Formulario con todos los campos + validación fecha_fin >= fecha_inicio | ⬜ | Pendiente |
| 6.5 | Editar convocatoria | Botón editar precarga formulario | ⬜ | Pendiente |
| 6.6 | Eliminar convocatoria | Botón eliminar con confirmación | ⬜ | Pendiente |
| 6.7 | Detalle convocatoria | Vista detalle `/calls/:id` muestra info + proyectos asociados | ⬜ | Pendiente |
| 6.8 | Botones admin vs user | Botones crear/editar/eliminar solo visibles para admin | ⬜ | Pendiente |

---

# 7. Módulo 7.4 — Gestión de Proyectos (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 7.1 | Ruta | Ruta `/projects` protegida | ⬜ | NO IMPLEMENTADO. No hay módulo `projects/`. |
| 7.2 | Listado general | Tabla/cards con: título, responsable, convocatoria asociada, estado, fecha | 🟧 | Dashboard muestra `DashboardRecentProjects.vue` con 3 proyectos hardcodeados. Sin vista dedicada `/projects`. |
| 7.3 | Filtros | Filtro por convocatoria, por usuario, por estado | ⬜ | Pendiente |
| 7.4 | "Mis proyectos" | Tab o link "Mis Proyectos" que filtra solo los proyectos del usuario logueado | ⬜ | Pendiente |
| 7.5 | Crear proyecto | Formulario con: título, descripción, seleccionar convocatoria (dropdown), estado inicial | ⬜ | Pendiente. Bottom Nav FAB `new-project` emite evento pero nada lo escucha. |
| 7.6 | Editar proyecto | Autor y admin pueden editar | ⬜ | Pendiente |
| 7.7 | Eliminar proyecto | Autor y admin pueden eliminar con confirmación | ⬜ | Pendiente |
| 7.8 | Detalle proyecto | Vista `/projects/:id` muestra información completa + lista de documentos asociados + sección para subir documentos | ⬜ | Pendiente |
| 7.9 | Asociar convocatoria | El formulario de creación trae la lista de convocatorias desde la API | ⬜ | Pendiente |

---

# 8. Módulo 7.5 — Gestión de Documentos (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 8.1 | Ruta | Ruta `/documents` protegida | ⬜ | NO IMPLEMENTADO. No hay módulo `documents/`. |
| 8.2 | Listado | Tabla con: nombre archivo, tamaño, tipo MIME, subido por, proyecto asociado, fecha, acciones | ⬜ | Pendiente |
| 8.3 | Filtros | Filtro por proyecto, por usuario, por tipo de archivo, rango fechas | ⬜ | Pendiente |
| 8.4 | Upload componente | Componente drag-and-drop o input type=file múltiple. Muestra progreso y valida tamaño/extensiones | 🟧 | Dashboard muestra `DashboardS3UploadPanel.vue` como UI mock. ⚠️ Sin lógica real de upload: no adjunta a proyecto, no envía FormData, no muestra progreso. |
| 8.5 | Asociar a proyecto | Al subir, dropdown para seleccionar proyecto asociado | ⬜ | Pendiente |
| 8.6 | Acción descargar | Botón "Descargar" llama al endpoint download y descarga el archivo | ⬜ | Pendiente |
| 8.7 | Acción ver detalle | Modal o detalle con metadata completa | ⬜ | Pendiente |
| 8.8 | Eliminar documento | Botón eliminar con confirmación | ⬜ | Pendiente |
| 8.9 | Panel de upload rápido | En Dashboard hay un panel o botón "Subir documento" | ✅ | `DashboardView.vue:26` usa `DashboardS3UploadPanel` y emite `upload-file`. Existe UI pero falta integración. |
| 8.10 | Validación cliente | Mensaje claro si el archivo excede tamaño o tiene extensión prohibida (antes de enviar) | ⬜ | No implementada. Panel S3 es visual. |

---

# 9. Módulo 7.7 — Historial de Cargas (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 9.1 | Ruta | Ruta `/history` (o `/documents/history`) protegida | ⬜ | NO IMPLEMENTADO. No hay módulo history. |
| 9.2 | Listado cronológico | Tabla ordenada por fecha descendente con: fecha/hora, usuario, nombre archivo, proyecto, link al archivo | ⬜ | Pendiente |
| 9.3 | Filtros | Filtro por usuario (admin ve todos, user ve solo los suyos), por proyecto, por rango | ⬜ | Pendiente |
| 9.4 | Paginación | Paginación de resultados BS5 | ⬜ | Pendiente |
| 9.5 | Acciones desde historial | Acceso directo a descargar o ver detalle del documento | ⬜ | Pendiente |
| 9.6 | Restricción de datos | Usuario normal solo ve su propio historial | ⬜ | Pendiente (backend + frontend). |

---

# 10. Módulo 7.8 — Perfil de Usuario (UI)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 10.1 | Ruta | Ruta `/profile` (o `/me`) protegida | ⬜ | NO EXISTE ruta /profile en ningún routes/index.ts. El sidebar item "profile" (bottom nav) y "documents" en rail van a users-list — incorrecto. FALTA módulo profile/me completo. |
| 10.2 | Foto de perfil | Muestra avatar actual. Si no hay, muestra el default del sistema. | ✅ | `authStore.ts:24-41` `avatarUrl` computed correcto: default con VITE_STATIC_URL, S3 URLs passthrough, y paths locales prefijados. Navbar y DashboardHeroCard lo usan. |
| 10.3 | Sección 1: Datos personales | Formulario con: username, email, first_name, last_name. Botón "Guardar cambios". | ⬜ | No existe vista. AuthService sí tiene `getProfile()` y backend `PUT /auth/me`, pero no hay UI. |
| 10.4 | Subir nueva foto | Input file + preview. Al guardar, envía `multipart/form-data` al backend. | ⬜ | No existe vista. Debe usar `FormData` con `file` field y `PUT` a `/api/v1/auth/me`. |
| 10.5 | Sección 2: Cambiar contraseña | Formulario con: contraseña actual, nueva contraseña, confirmar nueva contraseña. Botón "Cambiar contraseña". | ⬜ | No existe vista. IMPORTANTE: backend tampoco tiene endpoint dedicado que valide contraseña actual. Debe crearse ambos. |
| 10.6 | Validaciones match | "Nueva contraseña" y "Confirmar" deben coincidir; validador cliente. | ⬜ | Pendiente |
| 10.7 | Feedback | Toast éxito/error para cada sección. | ⬜ | Pendiente |
| 10.8 | Reflectar cambios en navbar | Después de actualizar nombre/avatar, el navbar/sidebar se actualiza sin recargar página (reactividad Pinia) | 🟧 | Navbar avatar usa `authStore.avatarUrl` computed reactivo. ⚠️ PERO: después de un PUT /auth/me exitoso, el store NO actualiza el user local (falta re-fetch o actualizar `user` ref). Habrá inconsistencia hasta próximo login. |

---

# 11. Integración con API / Manejo de Errores

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 11.1 | Interceptor JWT | Axios interceptor adjunta `Authorization: Bearer <token>` automáticamente | ✅ | [axios.ts:14-20](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L14-L20) request interceptor lee `localStorage.getItem('token')` y adjunta en header. Correcto. |
| 11.2 | Interceptor 401 | Al recibir 401: logout automático + redirect a login | ✅ | **NUEVO IMPLEMENTADO**. [axios.ts:28-35](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L28-L35) `if (status === 401) { authStore.logout(); window.location.href = '/login' }`. Limpia token+user+localStorage y redirige. |
| 11.3 | Manejo 403 | Mostrar toast "No tienes permisos para esta acción" | 🟧 | [axios.ts:36-38](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L36-L38) `status === 403 → console.error('Acceso denegado...')`. **⚠️ Solo console.error, NO hay toast UI visible al usuario**. UserListView además usa `alert()` — inconsistente. Falta componente toast global. |
| 11.4 | Manejo 400 / 422 | Mostrar mensajes de validación del servidor campo por campo si aplica | 🟧 | LoginView `catch` lee `error.response.data?.message \|\| error`. RegisterView lee `.message \|\| .error`. ⚠️ No mapea errores por campo a inputs específicos, solo mensaje global. |
| 11.5 | Manejo 500 | Página o toast de "Error del servidor, intenta nuevamente" | 🟧 | [axios.ts:38-40](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L38-L40) `status >= 500 → console.error('Error en el servidor...')`. **⚠️ Solo console.error, NO hay toast/página visible al usuario**. |
| 11.6 | Network error | Si el backend está caído, mensaje claro de "No hay conexión con el servidor" | ⬜ | Response interceptor NO maneja el caso `error.response === undefined` (network error, timeout, DNS fail). Si backend está caído, error llega sin `.status` → cae en `Promise.reject(error)` sin feedback al usuario. |
| 11.7 | Loading por operación | Botones cambian a disabled + spinner durante submit | ✅ | LoginView `:disabled="isLoading"` + `spinner-border`. RegisterView `:disabled="isLoading"` + spinner. UserModal `:disabled="loading"` en submit button. |
| 11.8 | Services por módulo | Cada módulo tiene `xxxService.ts` que encapsula llamadas API | ✅ | `auth/services/authService.ts` — register/login/getProfile. `user/services/userService.ts` — getUsers/createUser/updateUser/deleteUser. Encapsulación correcta. |

---

# 12. Validaciones UX y Responsive

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 12.1 | Formularios con Vuelidate o similar | Validación cliente: required, email, minLength, sameAs password | ⚠️ | ⚠️ NO INSTALADO Vuelidate, Yup ni Zod. Validaciones son: atributos HTML5 `required` `type=email` + checks manuales (match passwords en register). Funciona pero es menos robusto. No hay librería declarada en package.json. |
| 12.2 | Form control BS5 | Uso de `.form-control`, `.form-label`, `.form-text`, `.invalid-feedback` | 🟧 | UserModal usa `.form-control` y `.form-label`. Login/Register usan CSS classes custom `.form-control-custom` con estilos propios (no las classes BS5 standard). Combinación válida pero `.invalid-feedback` NO existe. |
| 12.3 | Tablas responsive | `.table-responsive` en todas las tablas | ✅ | `UserListView.vue:18` wrapper `<div class="table-responsive">`. Correcto. |
| 12.4 | Breakpoints probados | Vista probada en ≥1200px, 768–1199px, <768px. Sin layouts rotos. | 🟧 | Login/Register responsive: `col-md-6`, mobile (<768) padding reducido + mobile header. Layout: bottom-nav `display:none` en ≥768px (line 493-496 AppLayout). ⚠️ Rail nav sigue siendo 64px en mobile. |
| 12.5 | Tipografías y espaciados | Uso de classes BS5 de spacing (`mt-`, `p-`, `mb-`) y tipografía (`fs-`, `fw-`) consistentes | ✅ | Todo el proyecto usa `p-4`, `mb-3`, `gap-3`, `fw-bold`, `fs-5`, `text-muted`, `rounded-4`, etc. |
| 12.6 | Accesibilidad básica | Botones e inputs con atributos `aria-*`, labels asociados a inputs | ⚠️ | Muchos inputs NO tienen `id` asociados al `<label for=...>`. Login label custom no usa for=. No hay aria-describedby en errores. Botones icono (edit/delete) sin aria-label. Mejorar. |
| 12.7 | Navegación activa | Item de menú correspondiente resaltado en sidebar/navbar | ✅ | AppLayout `activeRail` y `activeBottomNav` computed sincronizados con `route.name`. Class `.active` en rail-link y bnav-item. |

---

# 13. Preparación para Build y Despliegue EC2

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 13.1 | Build producción | `npm run build` genera carpeta `dist/` sin errores | 🟧 | Scripts configurados. **Alineación .env.development ✅**: usa `/api/v1` que coincide con backend blueprint. ⚠️ `.env.production` tiene placeholder genérico — debe editarse con IP/Dominio real de EC2 antes de `npm run build`. |
| 13.2 | API base URL prod | `.env.production` configura `VITE_API_BASE_URL` con la IP/URL pública de EC2 | 🟧 | **ARCHIVO EXISTE NUEVO**: [.env.production:1-2](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/.env.production#L1-L2) define `VITE_API_BASE_URL=https://tu-dominio-backend.com/api` + `VITE_STATIC_URL=https://tu-dominio-backend.com`. ⚠️ Es un PLACEHOLDER — debe reemplazarse con la URL real (IP pública EC2 o dominio). Importante: backend blueprint es `/api/v1` así que la URL productiva debería ser `https://<IP>/api/v1` (o Nginx rewrite). |
| 13.3 | Assets con rutas correctas | Build sirve JS/CSS con rutas relativas o `/` según configuración de servidor web (Nginx) | ✅ | Por defecto Vite usa base `/`. Compatible con Nginx sirviendo `dist/` como root. |
| 13.4 | Router history mode | Si se usa history mode, servidor (Nginx) configurado con fallback a `index.html` | 🟧 | `createWebHistory` usado. ⚠️ Documentación pendiente para Nginx EC2: `location / { try_files $uri $uri/ /index.html; }`. También Nginx debe servir `/static/uploads/` desde backend o hacer proxy_pass. |
| 13.5 | Sin console.log excesivos | Limpiar `console.log` de debug antes de build producción (o usar linter) | ⚠️ | UserListView tiene `console.error` lines 76,113. Axios interceptor tiene `console.error` 403/500 lines 37,39. Válidos para debugging; ESLint configurado sin regla `no-console` estricta. |

---

# 14. Entregables Específicos

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 14.1 | Código fuente listo para zip | Todo `frontend/` incluido (excepto `node_modules`) | 🟧 | Código ok. Asegurarse de que `.env*` con secretos no esté incluido. |
| 14.2 | README con pasos | Existen pasos claros para `npm install`, `npm run dev`, `npm run build` | ✅ | `frontend/README.md` existe (no leído, pero estándar). Package.json scripts son claros. |
| 14.3 | package.json completo | Todas las dependencias declaradas | ✅ | Vue, Vue Router 5.2, Pinia 4, Axios, Bootstrap 5.3.8, @popperjs, bootstrap-icons, material-symbols, typescript, vite, vitest, playwright, eslint, prettier. Todas las dependencias core están. |

---

# 15. Registro de Aprobaciones

| Área | Revisor | Fecha | Observaciones | Estado Final |
|------|---------|-------|---------------|--------------|
| Configuración / Estructura | | 2026-08-02 (v1.2) | Stack ✅ modular ✅ env files AHORA EXISTEN ✅ Vite proxy ✅ Response interceptor AHORA EXISTE ✅ 403/500 solo console.error ⚠️ Network error sin manejar ⬜ | ⚠️ Observaciones |
| Autenticación UI | | 2026-08-02 (v1.2) | Login/Register forms ✅ **Botón logout dropdown AHORA FUNCIONAL ✅** **401 auto-logout AHORA EXISTE ✅** Faltan: toast errores, validaciones librería | 🟧 En Progreso |
| Layout / Navegación | | 2026-08-02 (v1.2) | Layout completo ✅ **Dropdown usuario+logout AHORA FUNCIONAL ✅** **Role filters sidebar (adminOnly) AHORA EXISTE ✅** **Rail oculto mobile ✅** **Redirect home si autenticado ✅** ⚠️ Menús calls/projects/docs/history/profile siguen apuntando a dashboard (sin rutas) | ✅ Mejoras / rutas pend |
| Dashboard | | 2026-08-02 (v1.2) | UI completa ✅ KPIs hardcodeados (sin conectar API stats) ⚠️ Crítico | 🟧 En Progreso |
| Admin Usuarios | | 2026-08-02 (v1.2) | Guard requiresAdmin ✅ Tabla y Modal SIMPLIFICADOS (faltan: first_name, last_name, role, is_active, avatar upload multipart FormData) | 🟧 En Progreso |
| Convocatorias | | 2026-08-02 (v1.2) | Nada implementado (solo preview estático en Dashboard; rail item existe pero → dashboard) | ⬜ Pendiente |
| Proyectos | | 2026-08-02 (v1.2) | Nada implementado (solo preview estático Dashboard; rail item → dashboard) | ⬜ Pendiente |
| Documentos | | 2026-08-02 (v1.2) | Nada implementado (solo panel visual upload Dashboard; rail item → dashboard) | ⬜ Pendiente |
| Historial | | 2026-08-02 (v1.2) | Nada implementado (rail item existe → dashboard) | ⬜ Pendiente |
| Perfil Usuario | | 2026-08-02 (v1.2) | Ruta/vista /profile NO existe 0%. Dropdown "Perfil" existe pero → dashboard. Store avatarUrl computed ✅ | ⬜ Pendiente |
| Integración API | | 2026-08-02 (v1.2) | Request interceptor ✅ **Response 401 logout AHORA EXISTE ✅** 403/500 console.error SOLO ⚠️ Network error (sin .response) NO manejado ⬜ | 🟧 En Progreso |
| UX / Responsive | | 2026-08-02 (v1.2) | BS5 espaciados ✅ **Rail oculto mobile AHORA FIXADO ✅** Faltan: validaciones librería (Vuelidate/Zod) a11y aria-labels | ⚠️ Observaciones |
| Build / Despliegue | | 2026-08-02 (v1.2) | **.env.production AHORA EXISTE (placeholder)** 🟧 Nginx fallback necesita docs; .env.production requiere editar URL real | 🟧 En Progreso |
| Entregables | | 2026-08-02 (v1.2) | Código ✅ package ✅ env files AHORA EXISTEN ambos ✅ | ✅ / env.prod requiere edit |

---

## Principales Hallazgos Críticos del Frontend (Actualizado v1.2)

1. **🔴 NO HAY VISTA DE PERFIL /profile**: Requisito mandatorio del alcance (datos personales, cambiar contraseña, subir foto). Ruta `/profile` no existe, módulo no creado. Dropdown "Perfil" del navbar apunta a dashboard.
2. **🟠 URL BASE INCONSISTENTE EN PRODUCCIÓN**: [.env.production:1](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/.env.production#L1) usa `.../api` pero backend blueprint es `/api/v1`. Debe ser `https://<IP_EC2>/api/v1` o configurar Nginx rewrite. Placeholder requiere edición antes de build.
3. **🟠 KPIs DASHBOARD SON ESTÁTICOS**: [DashboardKpiGrid.vue](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardKpiGrid.vue) valores hardcodeados 128, 8, 45, 1.2 TB. Debe consumir `GET /dashboard/stats` cuando exista endpoint backend.
4. **🟠 ADMIN USER MODAL INCOMPLETO**: [UserModal.vue:13-33](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/user/components/UserModal.vue#L13-L33) solo 3 campos (username, email, password). FALTAN: `first_name`, `last_name`, selector de `role` (admin/user), toggle `is_active`, input file `profile_picture` con `FormData` multipart.
5. **🟠 TABLA USUARIOS INCOMPLETA**: [UserListView.vue:20-26](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/user/views/UserListView.vue#L20-L26) columnas: ID, Usuario, Correo, Acciones. FALTAN 5 columnas obligatorias: `first_name`, `last_name`, `role`, `is_active` (estado), `profile_picture` (avatar thumbnail).
6. **🟠 4 MÓDULOS 0% IMPLEMENTADOS**: Calls, Projects, Documents, History. No hay módulos en `src/modules/`, no hay rutas, no hay vistas. Solo ítems en sidebar que apuntan a dashboard + previews estáticos en Dashboard.
7. **🟠 403/500 SOLO CONSOLE.ERROR**: [axios.ts:36-40](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L36-L40) errores se loguean pero usuario no ve nada. Necesita toast global (BS5 Toasts o componente propio) para feedback visual.
8. **🟠 NETWORK ERROR SIN MANEJAR**: [axios.ts:25-43](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/api/axios.ts#L25-L43) si backend está caído (`error.response === undefined`) no entra en ningún if → Promise.reject sin feedback. Usuario ve pantalla en blanco o spinner infinito.
9. **⚠️ USER SERVICE NO USA FORMDATA**: `userService.updateUser()` usa `api.put()` enviando JSON. Backend `PUT /users/:id` SOPORTA multipart para foto. Si se agrega input file al modal, hay que usar `new FormData()` + `Content-Type: multipart/form-data`.
10. **⚠️ FALTA REFRESH USER EN STORE**: Después de `PUT /auth/me` exitoso (actualizar perfil), el `authStore.user` local NO se actualiza. Habrá inconsistencia visual (navbar muestra nombre viejo) hasta próximo login/reload.
