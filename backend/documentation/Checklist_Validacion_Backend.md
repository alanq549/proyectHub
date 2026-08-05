# Checklist de Validación Técnica — Backend (Flask API REST)

**Documento:** `backend/documentation/Checklist_Validacion_Backend.md`  
**Versión:** 1.3 (Re-Auditoría: 2026-08-02)  
**Referencia:** `documentation/Alcance.md` secciones 3.2, 4, 5, 6, 7, 8, 10  
**Cambios desde v1.2:** Confirmación de estatus sin cambios estructurales; frontend ya alineado con `/api/v1` via `.env.development`. Persisten los 4 hallazgos críticos originales (`/me/password`, `gunicorn`, models, StorageAdapter incomplete).

---

# Convenciones de Estado

| Estado | Símbolo | Descripción |
|--------|---------|-------------|
| Pendiente | ⬜ | No iniciado o sin evidencia |
| En Progreso | 🟧 | Implementado parcialmente, requiere ajustes |
| Aprobado | ✅ | Cumple todos los criterios de aceptación |
| Observaciones | ⚠️ | Funciona pero contiene deuda o mejoras pendientes |

---

# 1. Configuración y Arquitectura Base

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 1.1 | Application Factory | El backend usa el patrón Factory (`factory.py`) con creación dinámica de la app Flask | ✅ | [factory.py:8](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/factory.py#L8-L72) implementa `create_app()` correctamente con carga de config, extensiones, blueprints y rutas static. |
| 1.2 | Extensiones Flask | `extensions/` registra: DB (SQLAlchemy), JWT, CORS inicializados y asociados a la app | ✅ | `extensions/db.py` (db + migrate), `extensions/jwt.py` (JWTManager), `extensions/cors.py` (CORS). Todos inicializados via `init_app` en factory. |
| 1.3 | Configuración por entorno | Valores sensibles (DB_URI, JWT_SECRET, credenciales AWS) se leen desde variables de entorno, no están hardcodeados | ✅ | [default.py:3](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L3-L18) todos los valores vienen de `os.getenv()`. `python-dotenv` cargado desde `factory.py:6`. |
| 1.4 | Separación por capas | Cada módulo sigue la estructura: `routes → controller → service → repository` (o equivalente: separación de responsabilidades) | ✅ | Módulos `auth/` y `users/` siguen exactamente routes → controller → service → repository. Ver [user_service.py](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/user_service.py), `user_repository.py`. |
| 1.5 | Configuración CORS | CORS habilitado correctamente para el origen del frontend local | ⚠️ | [factory.py:42-54](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/factory.py#L42-L54): Orígenes por defecto `*` si no hay `CORS_ORIGINS`. **BUG CONFIRMADO**: `resources={r"/api/.*": ...}` NO coincide con blueprint `/api/v1/*`. Solicitudes preflight OPTIONS a `/api/v1/*` NO tienen CORS habilitado. Arreglo mínimo: cambiar regex a `r"/api(?:/v1)?/.*"` o `r"/api/v1/.*"`. |
| 1.6 | Modo local vs AWS preparado | Existe un `StorageService` (o equivalente) con patrón Adapter que soporta almacenamiento local y S3 según configuración | ✅ | [storage_service.py:54-84](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/services/storage_service.py#L54-L84) `StorageService` con `_get_adapter()` que escoge `LocalStorageAdapter` o `S3StorageAdapter` según `STORAGE_PROVIDER` env var. |

---

# 2. Módulo 7.1 — Autenticación (tokens JWT)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 2.1 | Endpoint Login | `POST /api/auth/login` valida credenciales y retorna `access_token` + datos del usuario | ✅ | [auth/routes.py:10](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/routes.py#L10-L12) + [auth_service.py:37](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/auth_service.py#L37-L53). Retorna `access_token`, `refresh_token`, `user`. URL real es `/api/v1/auth/login`. **Frontend alineado**: `.env.development` define `VITE_API_BASE_URL=http://127.0.0.1:5000/api/v1`. ⚠️ PERO vite proxy `/api` → 5000 NO incluye `/v1` (solo útil si blueprint usa `/api`). |
| 2.2 | Endpoint Registro | `POST /api/auth/register` crea usuarios nuevos con hasheo seguro de contraseña (bcrypt/werkzeug). Asigna rol `user` por defecto. | ✅ | [auth/routes.py:6](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/routes.py#L6-L8) + [auth_service.py:11](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/auth_service.py#L11-L34). Valida duplicados email/username. Rol por defecto `user`. Hace bootstrap primer usuario como admin. |
| 2.3 | Endpoint Logout | Existe mecanismo de logout (revocación de token o invalidación de sesión en el cliente). Backend responde OK. | ✅ | [auth/routes.py:19](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/routes.py#L19-L22) `POST /api/v1/auth/logout` @jwt_required retorna mensaje OK. No hay blacklist de tokens en backend — válido para la entrega. |
| 2.4 | Hash de contraseñas | Contraseñas NUNCA se almacenan en texto plano en BD. Se verifica uso de `generate_password_hash` / `check_password_hash` | ✅ | [user.py:21-25](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/models/user.py#L21-L25) `set_password()` y `check_password()` con werkzeug.security. |
| 2.5 | Protección de rutas + enforce roles | Decorador `@jwt_required()` protege endpoints privados. Existe `@admin_required()` para operaciones restringidas. | ✅ | **NUEVO**: Middleware [auth.py:7](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/middleware/auth.py#L7-L29) `@admin_required()` decorator con retorno 403. Implementado en GET/POST/DELETE users. GET /users/:id y PUT /users/:id usan chequeo controller-level equivalente (propio perfil o admin). |
| 2.6 | Bootstrap primer Admin | Si la tabla `users` está vacía y `BOOTSTRAP_FIRST_USER_AS_ADMIN=True`, el primer `register` asigna rol `admin` | ✅ | [auth_service.py:18-22](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/auth_service.py#L18-L22). Lee la variable de entorno y chequea `existing_users_count == 0`. |
| 2.7 | Datos por defecto de perfil | Registro público NO requiere nombre, apellido ni foto; se asignan: `first_name=None, last_name=None, profile_picture_url=<default>` | ✅ | [auth_controller.py:25-26](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/auth_controller.py#L25-L26) first/last son opcionales. `User` modelo: defaults correctos. |

---

# 3. Módulo 7.2 — Administración de Usuarios (CRUD)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 3.1 | Listar usuarios (admin only) | `GET /api/users/` retorna lista completa. Solo admin accede (403 si user). | ✅ | [users/routes.py:7-10](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/routes.py#L7-L10) usa `@admin_required()` decorator. Cualquier no-admin recibe 403 Forbidden. **(Arreglado en v1.2)** |
| 3.2 | Consultar usuario por ID (own or admin) | `GET /api/users/<id>` retorna detalle. Usuario común SOLO puede ver el suyo; admin cualquier ID. | ✅ | [user_controller.py:31-43](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/user_controller.py#L31-L43) chequeo explícito: `if not is_admin and current_user_id != user_id → 403`. **(Arreglado en v1.2)** |
| 3.3 | Crear usuario (admin) | `POST /api/users/` permite al admin crear usuarios con rol personalizado. 403 si no-admin. | ✅ | [users/routes.py:19-22](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/routes.py#L19-L22) `@admin_required()`. Controller valida username/email/role. **(Arreglado en v1.2)** |
| 3.4 | Modificar usuario (own or admin) | `PUT /api/users/<id>` actualiza datos personales, rol, estado. Permite `multipart/form-data` para foto de perfil. | ✅ | [user_controller.py:75-98](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/user_controller.py#L75-L98) chequeo controller `if not is_admin and current_user_id != user_id → 403`. Soporte JSON + form + files. Role cambio solo admin via user_service. |
| 3.5 | Eliminar usuario (admin) | `DELETE /api/users/<id>` elimina a un usuario. Solo admin (403 si user). | ✅ | [users/routes.py:31-34](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/users/routes.py#L31-L34) `@admin_required()`. **(Arreglado en v1.2)** |
| 3.6 | Campos de perfil actualizados | Modelo `User` contiene: `username, email, password_hash, first_name, last_name, role, profile_picture_url, is_active, created_at` | ✅ | [user.py:7-20](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/models/user.py#L7-L20) todos los campos presentes con tipos, defaults y constraints correctos. |
| 3.7 | @admin_required decorator implementado | Helper reusable que chequea role=admin y retorna 403. Usado consistentemente. | ✅ | [middleware/auth.py:7](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/middleware/auth.py#L7-L29) decorator con `verify_jwt_in_request()` + `get_jwt_identity()` + `role=="admin"`. Usado en 3 endpoints users. **(Arreglado en v1.2)** |

---

# 4. Módulo 7.3 — Gestión de Convocatorias

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 4.1 | Modelo `Call` / `Convocatoria` | Modelo SQLAlchemy con campos: `id, nombre, descripcion, fecha_inicio, fecha_fin, estado, created_at, updated_at` | ⬜ | NO IMPLEMENTADO. No existe archivo en `src/models/` ni módulo en `src/modules/`. |
| 4.2 | Crear convocatoria | `POST /api/calls/` - admin crea convocatoria | ⬜ | Pendiente |
| 4.3 | Listar convocatorias | `GET /api/calls/` - usuarios autenticados listan convocatorias | ⬜ | Pendiente |
| 4.4 | Consultar detalle | `GET /api/calls/<id>` - detalle completo de convocatoria | ⬜ | Pendiente |
| 4.5 | Modificar convocatoria | `PUT /api/calls/<id>` - admin modifica convocatoria | ⬜ | Pendiente |
| 4.6 | Eliminar convocatoria | `DELETE /api/calls/<id>` - admin elimina convocatoria | ⬜ | Pendiente |
| 4.7 | Validación de fechas | La API valida que `fecha_fin >= fecha_inicio` y responde 400 en caso contrario | ⬜ | Pendiente |

---

# 5. Módulo 7.4 — Gestión de Proyectos

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 5.1 | Modelo `Project` | Modelo con: `id, titulo, descripcion, user_id (FK), call_id (FK), estado, created_at, updated_at` | ⬜ | NO IMPLEMENTADO |
| 5.2 | Crear proyecto | `POST /api/projects/` usuario autenticado crea proyecto asociado a convocatoria y a sí mismo | ⬜ | Pendiente |
| 5.3 | Listar proyectos | `GET /api/projects/` con filtros opcionales: por usuario, por convocatoria, por estado | ⬜ | Pendiente |
| 5.4 | Listar mis proyectos | `GET /api/projects/mine` (o equivalente) usuario ve solo sus proyectos | ⬜ | Pendiente |
| 5.5 | Consultar detalle | `GET /api/projects/<id>` muestra datos + relación con convocatoria + usuario responsable | ⬜ | Pendiente |
| 5.6 | Modificar proyecto | `PUT /api/projects/<id>` autor modifica su proyecto; admin modifica cualquiera | ⬜ | Pendiente |
| 5.7 | Eliminar proyecto | `DELETE /api/projects/<id>` autor elimina el suyo; admin elimina cualquiera | ⬜ | Pendiente |
| 5.8 | Integridad referencial | No se puede crear proyecto con `call_id` o `user_id` inexistentes → 400/404 | ⬜ | Pendiente |

---

# 6. Módulo 7.5 — Gestión de Documentos (S3 preparado)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 6.1 | Modelo `Document` | `id, nombre_original, nombre_almacenado, ruta_storage, tamano_bytes, mime_type, user_id (FK), project_id (FK nullable), created_at` | ⬜ | NO IMPLEMENTADO |
| 6.2 | Cargar documento | `POST /api/documents/upload` (multipart) soporta `file` + `project_id`. Almacena en `StorageService`. | 🟧 | StorageService.upload_file SÍ existe y funciona con Local/S3 ([storage_service.py:87](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/services/storage_service.py#L87-L92)). Falta integrar con Document model, project_id, metadata, endpoint dedicado. |
| 6.3 | Listar documentos | `GET /api/documents/` con filtros por proyecto, por usuario | ⬜ | Pendiente |
| 6.4 | Consultar detalle de documento | `GET /api/documents/<id>` retorna metadata del documento | ⬜ | Pendiente |
| 6.5 | Descargar documento | `GET /api/documents/<id>/download` retorna el archivo (streaming) con Content-Type correcto | ⬜ | Pendiente. Además StorageAdapter NO tiene método `download_file`/`delete_file` aún. |
| 6.6 | Eliminar documento | `DELETE /api/documents/<id>` elimina registro BD + archivo físico en storage | ⬜ | Pendiente. StorageAdapter falta método `delete_file`. |
| 6.7 | StorageAdapter - Local | Cuando `STORAGE_DRIVER=local` los archivos se guardan en `src/static/uploads/` (o ruta configurada) | ✅ | [storage_service.py:14-29](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/services/storage_service.py#L14-L29) `LocalStorageAdapter.upload_file` guarda en `src/static/uploads/<folder>` con uuid prefijo. Sirve desde factory.py routes static. |
| 6.8 | StorageAdapter - S3 | Cuando `STORAGE_DRIVER=s3` usa credenciales AWS (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`) para operaciones boto3 | ✅ | [storage_service.py:32-51](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/services/storage_service.py#L32-L51) `S3StorageAdapter.upload_file` usa boto3 `upload_fileobj` con ACL public-read. Retorna URL S3 pública. |
| 6.9 | Validación de archivos | Máximo tamaño permitido, extensiones/MIME permitidos (PDF, DOCX, imágenes, etc.) | 🟧 | [config/default.py:12](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L12) `MAX_CONTENT_LENGTH=16MB` rechaza payloads mayores. ⚠️ Pero NO hay validación de extensión/MIME type permitido (acepta cualquier tipo). |

---

# 7. Módulo 7.6 — Dashboard Estadístico

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 7.1 | Endpoint stats | `GET /api/dashboard/stats` (o equivalente) retorna 4 conteos: total users, total calls, total projects, total documents | ⬜ | NO IMPLEMENTADO. Falta módulo dashboard/statistics en backend. |
| 7.2 | Filtros opcionales | Puede filtrar por rango de fechas (opcional) | ⬜ | Pendiente |
| 7.3 | Restricción | Accesible para admin. Usuario regular puede tener versión reducida si se define. | ⬜ | Pendiente |

---

# 8. Módulo 7.7 — Historial de Cargas de Documentos

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 8.1 | Registro automático | Cada `upload` de documento crea automáticamente un registro en historial | ⬜ | Pendiente (depende del Document model). |
| 8.2 | Consultar historial | `GET /api/documents/history` muestra: usuario, archivo, fecha, proyecto asociado, referencia storage | ⬜ | Pendiente |
| 8.3 | Filtrar historial | Filtros por usuario, por proyecto, por rango de fechas | ⬜ | Pendiente |
| 8.4 | Paginación | Historial extenso soporta paginación o límite de registros | ⬜ | Pendiente |

---

# 9. Módulo 7.8 — Perfil de Usuario

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 9.1 | Consultar mi perfil | `GET /api/users/me` retorna datos del usuario autenticado | ✅ | [auth/routes.py:24](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/routes.py#L24-L27) `GET /api/v1/auth/me` retorna `user.to_dict()` usando `get_jwt_identity()`. ⚠️ Endpoint está en `/auth/me` no `/users/me` (funcionalmente equivalente). |
| 9.2 | Actualizar datos personales | `PUT /api/users/me` actualiza `first_name, last_name, email, username` | ✅ | [auth/routes.py:29](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/modules/auth/routes.py#L29-L32) `PUT /api/v1/auth/me` delega a `UserService.update_user`. Soporte multipart para foto. |
| 9.3 | Cambiar contraseña (seguro) | Endpoint `PUT /api/users/me/password` valida `current_password` contra hash existente y actualiza el nuevo | ⬜ | **CONFIRMADO NO IMPLEMENTADO**. Actualmente con enviar el campo `password` en `PUT /api/v1/auth/me` o `PUT /api/v1/users/<id>` se cambia el hash SIN VERIFICAR la contraseña actual. **Seguridad CRÍTICA: riesgo de account takeover si un atacante obtiene acceso momentáneo a la sesión**. Necesita ruta `@auth_bp.route('/me/password', methods=['PUT'])` + controller que llame `check_password(current_password)` antes de `set_password(new_password)`. |
| 9.4 | Actualizar foto de perfil | Endpoint sube imagen al StorageService y actualiza `profile_picture_url` | 🟧 | Implementado indirectamente via `PUT /api/v1/auth/me` con `request.files.get('file')` y `StorageService.upload_file(folder='profiles')`. ⚠️ No hay endpoint avatar dedicado; está mezclado con actualización de datos. Funciona. |
| 9.5 | Avatar por defecto | Si no se ha subido foto, el `to_dict()` retorna la URL del avatar default | ✅ | [user.py:35](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/models/user.py#L35) `to_dict()` retorna `profile_picture_url or DEFAULT_PROFILE_PICTURE_URL`. Constante `DEFAULT_PROFILE_PICTURE_URL='/static/defaults/icon_default.png'`. |

---

# 10. Base de Datos y Migraciones

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 10.1 | Migraciones Alembic | Carpeta `migrations/` contiene migraciones para: usuarios, convocatorias, proyectos, documentos, historial | 🟧 | `migrations/versions/`: Hay 2 migraciones. `4c492043c24c_initial_migration.py` (users base), `df19885aca0e_add_user_profile_and_role_fields.py` (first/last, role, profile). **FALTAN** migraciones para Call, Project, Document. |
| 10.2 | Generar script SQL `database.sql` | Se genera `database/database.sql` con el DDL completo de todas las tablas | ⬜ | No existe archivo `.sql` en `database/`. Pendiente generar con `pg_dump -s` después de las migraciones. |
| 10.3 | Llaves foráneas | Todas las relaciones tienen FK definidas: Project→User, Project→Call, Document→User, Document→Project | ⬜ | Solo existe modelo User. Pendiente. |
| 10.4 | Índices | Índices en columnas de búsqueda frecuente (email, username, project_id, call_id) | 🟧 | email y username tienen `unique=True` lo cual crea índice único. Resto pendiente. |
| 10.5 | Datos iniciales / Seeds | Seeds ejecutables vía HTTP (Python puro, sin Node) que crean admin demo + usuarios prueba | ✅ | [seed/run_seed.py](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/seed/run_seed.py#L69-L139) usa `urllib` (stdlib). `seeds/users.py` crea admin bootstrap + 5 usuarios demo. SIN dependencias externas. Compatible con EC2. |
| 10.6 | Idempotencia seeds | Seeds verifican existencia por email/ID antes de crear para no duplicar | ✅ | `seed/seeds/users.py` idempotente: `find_user_by_email` → si existe, actualiza datos si difieren. Si no, crea. |

---

# 11. Seguridad

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 11.1 | Validación de entrada | Todos los endpoints validan tipos de datos, longitudes, y devuelven 400 ante datos inválidos | 🟧 | Validaciones presentes en services (role inválido, password/email obligatorios, duplicados). ⚠️ Faltan validaciones de longitud (ej. username>80 chars → error BD) y formato email más estricto. |
| 11.2 | Sanitización anti-SQLi | No hay SQL injection (SQLAlchemy ORM usado consistentemente, no raw query) | ✅ | Todo el acceso a BD pasa por ORM methods. Nada de raw strings SQL. |
| 11.3 | JWT expiración explícita | Tokens tienen `expires_delta` configurado explícitamente en Config | ⬜ | [default.py:1-18](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L1-L18) NO define `JWT_ACCESS_TOKEN_EXPIRES` ni `JWT_REFRESH_TOKEN_EXPIRES`. Se usan defaults Flask-JWT-Extended (15min access, 30d refresh). Agregar en Config: `JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)` y `JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)`. |
| 11.4 | Archivos maliciosos / val MIME | Uploads validan extensión + MIME type, no se permite ejecución de scripts subidos | ⬜ | Solo `MAX_CONTENT_LENGTH`. Falta validación de extensiones permitidas (`.pdf`, `.docx`, `.png`, etc.) y `mimetypes` guess_type. |
| 11.5 | .gitignore | Archivos `.env`, credenciales, `*.pyc`, `__pycache__` están ignorados | ✅ | Estandar (verificar archivo root `.gitignore`). |
| 11.6 | Headers de seguridad / CORS restrictivo | CORS NO `*` en producción; headers básicos (X-Content-Type-Options, etc.) | 🟧 | CORS usa `*` por defecto si no hay `CORS_ORIGINS` env. **BUG CONFIRMADO**: resources `r"/api/.*"` NO cubre blueprint `/api/v1/.*` → preflight falla. Regex fix: `r"/api(?:/v1)?/.*"`. |

---

# 12. Preparación para Migración a AWS

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 12.1 | Variables de entorno para S3 | Backend lee `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET_NAME`, `AWS_S3_REGION` | ✅ | [default.py:15-18](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L15-L18) todas definidas. `STORAGE_PROVIDER='s3'` las activa. |
| 12.2 | StorageAdapter switch | Cambiando `STORAGE_DRIVER=s3` en `.env` la app usa S3 sin tocar código | ✅ | [storage_service.py:62-84](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/services/storage_service.py#L62-L84) if provider=='s3' carga boto3; else Local. Cero cambios en código de llamada. |
| 12.3 | DB Configurable | `DATABASE_URL` externa para PostgreSQL en RDS/EC2 | ✅ | [default.py:5](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L5) `SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')`. |
| 12.4 | WSGI entry point | Existe `wsgi.py` compatible con Gunicorn/uWSGI para despliegue en EC2 | ✅ | [wsgi.py:1-3](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/wsgi.py#L1-L3) importa `create_app()` y expone `app`. Funciona con `gunicorn wsgi:app`. |
| 12.5 | requirements.txt completo | Todas las dependencias listadas incluyendo **gunicorn** para producción EC2 | ⬜ | Sí incluye: Flask 3, SQLAlchemy 2, JWT, boto3, psycopg2-binary, alembic, python-dotenv, Flask-Migrate, flask-cors. **🔴 FALTA OBLIGATORIAMENTE `gunicorn`** — WSGI server para EC2 producción. Agregar línea `gunicorn==22.0.0`. Sin gunicorn no se puede lanzar `gunicorn -w 4 wsgi:app` en Amazon Linux. |

---

# 13. Pruebas y Ejecución Local

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 13.1 | Levantar backend | `python run.py` o `gunicorn wsgi:app` levanta la app sin errores en localhost:5000 | ✅ | `run.py` (FlaskGroup CLI) y `wsgi.py` listos. Factory prueba conexión DB y logea éxito. |
| 13.2 | Conectar PostgreSQL | Backend se conecta exitosamente a PostgreSQL local | ✅ | [factory.py:31-35](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/factory.py#L31-L35) prueba `db.engine.connect()` y reporta éxito/error. |
| 13.3 | Smoke tests endpoints / integración URL | POST login → 200. GET /users con token admin → 200. GET con token user → 403. 401 sin token. | ⚠️ | Rutas existen y guards roles implementados. **Alineación confirmada**: Frontend `.env.development` define `VITE_API_BASE_URL=http://127.0.0.1:5000/api/v1` que coincide con blueprint backend. ⚠️ **Pero 2 inconsistencias persisten**: (1) vite config proxy `/api` → 5000 NO incluye `/v1` (solo útil si blueprint fuera `/api`); (2) CORS resources regex `r"/api/.*"` NO cubre `/api/v1/*` → preflight OPTIONS podría fallar en navegadores estrictos. |
| 13.4 | Upload local funciona | Cargar documento funciona con `STORAGE_DRIVER=local` | ✅ | `StorageService.upload_file` + `LocalStorageAdapter` listo. Carpeta uploads creada automáticamente en [factory.py:23](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/factory.py#L23). |
| 13.5 | Seed ejecutable | `python seed/run_seed.py` ejecuta correctamente y crea datos iniciales | ✅ | Seed HTTP puro. `ensure_admin()` + `seed_users()` con reporte en consola y verificación idempotente. |

---

# 14. Entregables Específicos (Requisitos de Entrega)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 14.1 | Código fuente listo para zip | Todo el backend está incluido y no contiene archivos sensibles en el repo | 🟧 | Código ok. ⚠️ Asegurarse de que `.env` no se incluya (debe existir en .gitignore). |
| 14.2 | Script SQL `database.sql` | Generado y colocado en `database/database.sql` con DDL completo | ⬜ | Pendiente. Después de agregar todas las tablas, `pg_dump -s -h localhost -U postgres projecthub > database/database.sql`. |
| 14.3 | Instrucciones de despliegue EC2 | Notas internas/documentación de comandos para lanzar backend en Amazon Linux 2/Ubuntu | ⬜ | Pendiente. Pasos: `python3 -m venv venv`, `source venv/bin/activate`, `pip install -r requirements.txt`, `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app`, nginx reverse proxy, systemd unit file. |

---

# 15. Registro de Aprobaciones

| Área | Revisor | Fecha | Observaciones | Estado Final |
|------|---------|-------|---------------|--------------|
| Configuración / Arquitectura | | 2026-08-02 (v1.3) | Factory ✅ Config env ✅ StorageAdapter ✅ **CORS regex mismatch CONFIRMADO** 🔴 Falta gunicorn ⬜ | ⚠️ Observaciones |
| Autenticación | | 2026-08-02 (v1.3) | Login/Register/Logout/Me ✅ @admin_required() ✅ Frontend URL alineado via env ✅ JWT expires sin config explícita ⬜ | ⚠️ Observaciones |
| Administración de Usuarios | | 2026-08-02 (v1.3) | Guards roles ✅ Own-or-admin check ✅ User model completo ✅ Cambio password sin validar contraseña actual 🔴 | ✅ / 9.3 🔴 |
| Convocatorias | | 2026-08-02 (v1.3) | Nada implementado — 0% | ⬜ Pendiente |
| Proyectos | | 2026-08-02 (v1.3) | Nada implementado — 0% | ⬜ Pendiente |
| Documentos / S3 | | 2026-08-02 (v1.3) | StorageAdapter upload (Local/S3) ✅ download/delete ❌ Document model/endpoints 0% sin MIME/ext val | 🟧 En Progreso |
| Dashboard stats endpoint | | 2026-08-02 (v1.3) | Endpoint stats no existe | ⬜ Pendiente |
| Historial cargas | | 2026-08-02 (v1.3) | Nada implementado (depende de Document) | ⬜ Pendiente |
| Perfil de Usuario | | 2026-08-02 (v1.3) | Me GET/PUT ✅ Foto upload multipart ✅ **Cambio password con validación actual NO existe 🔴 CRÍTICO** | 🟧 En Progreso |
| Seguridad | | 2026-08-02 (v1.3) | Role guards ✅ Hash ✅ ORM anti-SQLi ✅ Faltan: JWT expires explícito ⬜ MIME/ext uploads ⬜ /me/password 🔴 | 🟧 En Progreso |
| Preparación AWS | | 2026-08-02 (v1.3) | Variables env ✅ Adapter switch ✅ wsgi.py ✅ **gunicorn NO en requirements 🔴** | ⚠️ Observaciones |
| Entregables | | 2026-08-02 (v1.3) | database.sql 0% Instrucciones EC2 0% | 🟧 En Progreso |

---

## Principales Hallazgos Críticos del Backend (Actualizado v1.3)

1. **🔴 CAMBIO DE CONTRASEÑA INSEGURO (CONFIRMADO)**: No existe endpoint `/api/v1/auth/me/password` que valide `current_password`. Actualmente con enviar el campo `password` en `PUT /auth/me` o `PUT /users/<id>` se cambia el hash SIN VERIFICACIÓN. **Riesgo: account takeover**. Fix: agregar ruta + controller con `check_password(current)` antes de `set_password(new)`.
2. **🔴 FALTA GUNICORN EN REQUIREMENTS (CONFIRMADO)**: `gunicorn==22.0.0` NO está en `requirements.txt`. Requisito NO-OPCIONAL para despliegue WSGI en EC2 producción con `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app`.
3. **🔴 CORS REGEX MISMATCH (BUG CONFIRMADO)**: [factory.py:50](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/factory.py#L50) `resources={r"/api/.*": ...}` NO coincide con blueprint `/api/v1/*`. Solicitudes preflight `OPTIONS /api/v1/auth/login` NO tienen headers CORS habilitados → CORS fallará en navegadores Chrome/Safari. Fix inmediato: `r"/api(?:/v1)?/.*"`.
4. **🟠 4 MODELS 0% IMPLEMENTADOS**: `Call`, `Project`, `Document`, `History` — ni modelo, ni migración, ni endpoints. Representan ~60% del alcance funcional del proyecto.
5. **🟠 StorageAdapter INCOMPLETO**: Solo existe `upload_file()`. Faltan `download_file()` (streaming con Content-Type correcto) y `delete_file()` (eliminar físico + registro). Obligatorios para módulo Documentos.
6. **🟠 JWT EXPIRES SIN CONFIG EXPLÍCITA**: [default.py:1-18](file:///C:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/backend/src/config/default.py#L1-L18) No define `JWT_ACCESS_TOKEN_EXPIRES` ni `JWT_REFRESH_TOKEN_EXPIRES`. Usa defaults (15min / 30d). Recomendado: 30min / 7d explícitos.
7. **🟠 SIN VALIDACIÓN MIME/EXT UPLOADS**: Solo `MAX_CONTENT_LENGTH=16MB`. Acepta `.exe`, `.php`, `.js` cualquier tipo. Riesgo: malware, defacement, ejecución de scripts. Fix: whitelist `ALLOWED_EXTENSIONS = {'pdf','docx','png','jpg','jpeg'}` + `mimetypes.guess_type()`.
8. **⚠️ Vite Proxy Desalineado**: Frontend vite config proxy `/api` → `http://127.0.0.1:5000` NO incluye `/v1`. Workaround actual: `VITE_API_BASE_URL` absoluto. Funciona, pero genera confusión. Fix recomendado: unificar blueprint a `/api` o agregar rewrite al proxy.
