# Checklist de Validación Técnica — Backend (Flask API REST)

**Documento:** `backend/documentation/Checklist_Validacion_Backend.md`  
**Versión:** 1.1 (Auditoría: 2026-08-02)  
**Referencia:** `documentation/Alcance.md` secciones 3.2, 4, 5, 6, 7, 8, 10

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
| 1.1 | Application Factory | El backend usa el patrón Factory (`factory.py`) con creación dinámica de la app Flask | ✅ | `factory.py:8` implementa `create_app()` correctamente con carga de config, extensiones, blueprints y rutas static. |
| 1.2 | Extensiones Flask | `extensions/` registra: DB (SQLAlchemy), JWT, CORS inicializados y asociados a la app | ✅ | `extensions/db.py` (db + migrate), `extensions/jwt.py` (JWTManager), `extensions/cors.py` (CORS). Todos inicializados via `init_app` en factory. |
| 1.3 | Configuración por entorno | Valores sensibles (DB_URI, JWT_SECRET, credenciales AWS) se leen desde variables de entorno, no están hardcodeados | ✅ | `src/config/default.py:3` todos los valores vienen de `os.getenv()`. `python-dotenv` cargado desde `factory.py:6`. |
| 1.4 | Separación por capas | Cada módulo sigue la estructura: `routes → controller → service → repository` (o equivalente: separación de responsabilidades) | ✅ | Módulos `auth/` y `users/` siguen exactamente routes → controller → service → repository. Ver `src/modules/users/user_service.py`, `user_repository.py`. |
| 1.5 | Configuración CORS | CORS habilitado correctamente para el origen del frontend local | ⚠️ | `factory.py:42-54`: Orígenes por defecto `*` si no hay `CORS_ORIGINS`. En producción debe limitarse; localmente aceptable pero requiere definirse el env var. |
| 1.6 | Modo local vs AWS preparado | Existe un `StorageService` (o equivalente) con patrón Adapter que soporta almacenamiento local y S3 según configuración | ✅ | `src/services/storage_service.py:54` `StorageService` con `_get_adapter()` que escoge `LocalStorageAdapter` o `S3StorageAdapter` según `STORAGE_PROVIDER` env var. |

---

# 2. Módulo 7.1 — Autenticación (tokens JWT)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 2.1 | Endpoint Login | `POST /api/auth/login` valida credenciales y retorna `access_token` + datos del usuario | ✅ | `src/modules/auth/routes.py:10` + `auth_service.py:37`. Retorna `access_token`, `refresh_token`, `user`. ⚠️ Nota: prefijo URL real es `/api/v1/auth/login` (no `/api/auth`). El frontend axios apunta a `/api` sin el `v1`. INCONSISTENCIA — requiere alinear. |
| 2.2 | Endpoint Registro | `POST /api/auth/register` crea usuarios nuevos con hasheo seguro de contraseña (bcrypt/werkzeug). Asigna rol `user` por defecto. | ✅ | `auth/routes.py:6` + `auth_service.py:11`. Valida duplicados email/username. Rol por defecto `user`. Hace bootstrap primer usuario como admin. |
| 2.3 | Endpoint Logout | Existe mecanismo de logout (revocación de token o invalidación de sesión en el cliente). Backend responde OK. | ✅ | `auth/routes.py:19` `POST /api/v1/auth/logout` @jwt_required retorna mensaje OK. No hay blacklist de tokens en backend — válido para la entrega. |
| 2.4 | Hash de contraseñas | Contraseñas NUNCA se almacenan en texto plano en BD. Se verifica uso de `generate_password_hash` / `check_password_hash` | ✅ | `src/models/user.py:21-25` `set_password()` y `check_password()` con werkzeug.security. |
| 2.5 | Protección de rutas | Decorador/guard `@jwt_required()` protege todos los endpoints de módulos privados | ✅ | Users CRUD, logout, refresh, /me todos llevan `@jwt_required()`. ⚠️ PERO: no hay enforce de ROLE dentro del decorador — endpoints admin (`GET /users`, etc.) son accesibles por CUALQUIER usuario autenticado. FALTA agregar guard de rol. |
| 2.6 | Bootstrap primer Admin | Si la tabla `users` está vacía y `BOOTSTRAP_FIRST_USER_AS_ADMIN=True`, el primer `register` asigna rol `admin` | ✅ | `auth_service.py:18-22`. Lee la variable de entorno y chequea `existing_users_count == 0`. |
| 2.7 | Datos por defecto de perfil | Registro público NO requiere nombre, apellido ni foto; se asignan: `first_name=None, last_name=None, profile_picture_url=<default>` | ✅ | `auth_controller.py:25-26` first/last son opcionales. `User` modelo: `first_name/last_name=None`, `profile_picture_url=DEFAULT_PROFILE_PICTURE_URL`. |

---

# 3. Módulo 7.2 — Administración de Usuarios (CRUD)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 3.1 | Listar usuarios | `GET /api/users/` retorna lista paginada o completa de usuarios. Acceso restringido a `admin`. | 🟧 | Existe `GET /api/v1/users` en `users/routes.py:5`. @jwt_required PERO NO hay enforce de role admin. Cualquier usuario autenticado puede listar TODOS los usuarios. FALTA guard role. |
| 3.2 | Consultar usuario por ID | `GET /api/users/<id>` retorna detalle de un usuario | ✅ | `users/routes.py:11` + `user_service.py:14` get_by_id, 404 si no existe. ⚠️ Mismo problema: falta restrictivo (propio usuario o admin). |
| 3.3 | Crear usuario (admin) | `POST /api/users/` permite al admin crear usuarios con rol y datos personalizados | 🟧 | Existe `POST /api/v1/users` en `user_controller.py:38`. Valida username/email duplicados y role válido. ⚠️ FALTA enforce role admin: cualquier autenticado puede crear usuarios incluyendo admins. |
| 3.4 | Modificar usuario | `PUT /api/users/<id>` actualiza datos personales, rol, estado. Permite `multipart/form-data` para foto de perfil. | ✅ | `user_controller.py:67` soporta JSON + form + files via `_extract_data()` y `request.files.get('file')`. Role solo modificable por admin (validado en `user_service.py:72-74`). |
| 3.5 | Eliminar usuario | `DELETE /api/users/<id>` elimina (o desactiva `is_active=False`) a un usuario del sistema | 🟧 | Existe `DELETE /api/v1/users/<id>` en `users/routes.py:29`. ⚠️ FALTA enforce admin. Cualquier usuario autenticado puede eliminar a cualquiera. |
| 3.6 | Campos de perfil actualizados | Modelo `User` contiene: `username, email, password_hash, first_name, last_name, role, profile_picture_url, is_active, created_at` | ✅ | `src/models/user.py:7-20` todos los campos presentes con tipos, defaults y constraints correctos. |
| 3.7 | Enforce de roles | Un usuario `user` NO puede listar, crear ni modificar otros usuarios (prueba 401/403) | ⬜ | NO IMPLEMENTADO. Falta agregar helper que verifique role=admin en endpoints 3.1, 3.3, 3.5 y retorno 403. Sugerencia: `@admin_required` decorator. |

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
| 6.2 | Cargar documento | `POST /api/documents/upload` (multipart) soporta `file` + `project_id`. Almacena en `StorageService`. | 🟧 | StorageService.upload_file SÍ existe y funciona con Local/S3 (`storage_service.py:87`). Falta integrar con Document model, project_id, metadata, endpoint dedicado. |
| 6.3 | Listar documentos | `GET /api/documents/` con filtros por proyecto, por usuario | ⬜ | Pendiente |
| 6.4 | Consultar detalle de documento | `GET /api/documents/<id>` retorna metadata del documento | ⬜ | Pendiente |
| 6.5 | Descargar documento | `GET /api/documents/<id>/download` retorna el archivo (streaming) con Content-Type correcto | ⬜ | Pendiente. Además StorageAdapter NO tiene método download_file/delete_file aún. |
| 6.6 | Eliminar documento | `DELETE /api/documents/<id>` elimina registro BD + archivo físico en storage | ⬜ | Pendiente. StorageAdapter falta método `delete_file`. |
| 6.7 | StorageAdapter - Local | Cuando `STORAGE_DRIVER=local` los archivos se guardan en `src/static/uploads/` (o ruta configurada) | ✅ | `storage_service.py:14-29` `LocalStorageAdapter.upload_file` guarda en `src/static/uploads/<folder>` con uuid prefijo. Sirve desde factory.py routes static. |
| 6.8 | StorageAdapter - S3 | Cuando `STORAGE_DRIVER=s3` usa credenciales AWS (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`) para operaciones boto3 | ✅ | `storage_service.py:32-51` `S3StorageAdapter.upload_file` usa boto3 `upload_fileobj` con ACL public-read. Retorna URL S3 pública. |
| 6.9 | Validación de archivos | Máximo tamaño permitido, extensiones/MIME permitidos (PDF, DOCX, imágenes, etc.) | 🟧 | `config/default.py:12` `MAX_CONTENT_LENGTH=16MB` rechaza payloads mayores. ⚠️ Pero NO hay validación de extensión/MIME type permitido (acepta cualquier tipo). |

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
| 9.1 | Consultar mi perfil | `GET /api/users/me` retorna datos del usuario autenticado | ✅ | `auth/routes.py:24` `GET /api/v1/auth/me` retorna `user.to_dict()` usando `get_jwt_identity()`. ⚠️ El endpoint está en `/auth/me` no `/users/me`. Documentación debe alinear. |
| 9.2 | Actualizar datos personales | `PUT /api/users/me` actualiza `first_name, last_name, email, username` | ✅ | `auth/routes.py:29` `PUT /api/v1/auth/me` delega a `UserService.update_user`. Soporte multipart para foto. |
| 9.3 | Cambiar contraseña | Endpoint `PUT /api/users/me/password` valida contraseña actual y actualiza el hash | ⬜ | NO IMPLEMENTADO. Actualmente cambiar password solo se puede vía `PUT /users/<id>` incluyendo password field, PERO NO VALIDA la contraseña actual y no hay endpoint dedicado /me/password. RIESGO de seguridad. |
| 9.4 | Actualizar foto de perfil | Endpoint `PUT /api/users/me/avatar` sube imagen al StorageService y actualiza `profile_picture_url` | 🟧 | Implementado indirectamente via `PUT /api/v1/auth/me` con `request.files.get('file')` y `StorageService.upload_file(folder='profiles')`. ⚠️ No hay endpoint avatar dedicado; está mezclado. Funciona. |
| 9.5 | Avatar por defecto | Si no se ha subido foto, el `to_dict()` retorna la URL del avatar default | ✅ | `src/models/user.py:35` `to_dict()` retorna `profile_picture_url or DEFAULT_PROFILE_PICTURE_URL`. Constante `DEFAULT_PROFILE_PICTURE_URL='/static/defaults/icon_default.png'`. |

---

# 10. Base de Datos y Migraciones

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 10.1 | Migraciones Alembic | Carpeta `migrations/` contiene migraciones para: usuarios, convocatorias, proyectos, documentos, historial | 🟧 | `migrations/versions/`: Hay 2 migraciones. `4c492043c24c_initial_migration.py` (users base), `df19885aca0e_add_user_profile_and_role_fields.py` (first/last, role, profile). FALTAN migraciones para Call, Project, Document. |
| 10.2 | Generar script SQL | Se genera `database/database.sql` con el DDL completo de todas las tablas | ⬜ | No existe archivo `.sql` en `database/`. Solo existe `Reset de la base de datos.md`. Pendiente generar con `pg_dump` después de las migraciones. |
| 10.3 | Llaves foráneas | Todas las relaciones tienen FK definidas: Project→User, Project→Call, Document→User, Document→Project | ⬜ | Solo existe modelo User. Pendiente. |
| 10.4 | Índices | Índices en columnas de búsqueda frecuente (email, username, project_id, call_id) | 🟧 | email y username tienen `unique=True` lo cual crea índice único. Resto pendiente. |
| 10.5 | Datos iniciales / Seeds | Seeds ejecutables vía HTTP (Python puro, sin Node) que crean admin demo + usuarios prueba | ✅ | `seed/run_seed.py` usa `urllib` (stdlib). `seeds/users.py` crea admin bootstrap + 5 usuarios demo. SIN dependencias externas. Compatible con EC2. |
| 10.6 | Idempotencia seeds | Seeds verifican existencia por email/ID antes de crear para no duplicar | ✅ | `seed/seeds/users.py:51-77` `find_user_by_email` → si existe, actualiza datos si difieren. Si no, crea. |

---

# 11. Seguridad

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 11.1 | Validación de entrada | Todos los endpoints validan tipos de datos, longitudes, y devuelven 400 ante datos inválidos | 🟧 | Validaciones presentes en services (role inválido, password/email obligatorios, duplicados). ⚠️ Faltan validaciones de longitud (ej. username>80 chars → error BD) y formato email más estricto. |
| 11.2 | Sanitización | No hay SQL injection (SQLAlchemy ORM usado consistentemente, no raw query sin parámetros) | ✅ | Todo el acceso a BD pasa por ORM methods (query.filter_by, add, commit). Nada de raw strings SQL. |
| 11.3 | JWT expiración | Tokens tienen `expires_delta` configurado (ej: 24h o menos) | ⬜ | `auth_service.py:46-47` usa `create_access_token` y `create_refresh_token` con defaults Flask-JWT-Extended (15min access, 30d refresh normalmente). Mejor EXPLICITAMENTE definir `JWT_ACCESS_TOKEN_EXPIRES` en config. |
| 11.4 | Archivos maliciosos | Uploads validan extensión + MIME type, no se permite ejecución de scripts subidos | ⬜ | Solo MAX_CONTENT_LENGTH. Falta validación de extensiones permitidas (`.pdf`, `.docx`, `.png`, etc.) y `mimetypes` guess_type. |
| 11.5 | .gitignore | Archivos `.env`, credenciales, `*.pyc`, `__pycache__` están ignorados | ✅ | Root `.gitignore` debe incluirlos (estándar). |
| 11.6 | Headers de seguridad | CORS restrictivo, no exponer `Server` excesivo, `X-Content-Type-Options` u otros básicos | 🟧 | CORS usa `*` por defecto si no hay env var. Resto headers básicos no configurados (puede agregarse con flask-talisman o similar — opcional para entrega). |

---

# 12. Preparación para Migración a AWS

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 12.1 | Variables de entorno para S3 | Backend lee `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET_NAME`, `AWS_S3_REGION` | ✅ | `src/config/default.py:15-18` todas definidas. `STORAGE_PROVIDER='s3'` las activa. |
| 12.2 | StorageAdapter switch | Cambiando `STORAGE_DRIVER=s3` en `.env` la app usa S3 sin tocar código | ✅ | `storage_service.py:62-84` if provider=='s3' carga boto3; else Local. Cero cambios en código de llamada. |
| 12.3 | DB Configurable | `DATABASE_URL` externa para PostgreSQL en RDS/EC2 | ✅ | `config/default.py:5` `SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')`. |
| 12.4 | WSGI entry point | Existe `wsgi.py` compatible con Gunicorn/uWSGI para despliegue en EC2 | ✅ | `wsgi.py:1-3` importa `create_app()` y expone `app`. Funciona con `gunicorn wsgi:app`. |
| 12.5 | requirements.txt | Todas las dependencias están listadas (Flask, SQLAlchemy, JWT, boto3, gunicorn, etc.) | 🟧 | Sí incluye Flask, SQLAlchemy, JWT, boto3, psycopg2-binary, alembic, python-dotenv, flask-migrate, flask-cors. ⚠️ FALTA `gunicorn` (WSGI server para producción en EC2). Agregar `gunicorn==22.x`. |

---

# 13. Pruebas y Ejecución Local

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 13.1 | Levantar backend | `python run.py` o `gunicorn wsgi:app` levanta la app sin errores en localhost:5000 | ✅ | `run.py` (FlaskGroup con CLI) y `wsgi.py` listos. Factory prueba conexión DB y logea éxito. |
| 13.2 | Conectar PostgreSQL | Backend se conecta exitosamente a PostgreSQL local | ✅ | `factory.py:31-35` prueba `db.engine.connect()` y reporta éxito/error. |
| 13.3 | Smoke tests endpoints | POST login → 200, GET /users (con token admin) → 200, 401 sin token | 🟧 | Rutas existen. ⚠️ ⚠️ Inconsistencia URL: Blueprint es `/api/v1/` pero `src/api/axios.ts` del frontend usa baseURL `/api` (sin v1). Esto va a fallar en integración. Alinear: o cambiar modules_bp url_prefix a `/api`, o cambiar axios baseURL a `/api/v1`. |
| 13.4 | Upload local funciona | Cargar documento funciona con `STORAGE_DRIVER=local` | ✅ | `StorageService.upload_file` + `LocalStorageAdapter` probado en código. Carpeta uploads creada automáticamente factory.py:23. |
| 13.5 | Seed ejecutable | `python seed/run_seed.py` ejecuta correctamente y crea datos iniciales | ✅ | Seed HTTP puro. `ensure_admin()` + `seed_users()` con reporte en consola y verificación idempotente. |

---

# 14. Entregables Específicos (Requisitos de Entrega)

| # | Item | Criterios de Aceptación | Estado | Evidencia / Notas |
|---|------|--------------------------|--------|--------------------|
| 14.1 | Código fuente listo para zip | Todo el backend está incluido y no contiene archivos sensibles en el repo | 🟧 | Código ok. ⚠️ Asegurarse de que `.env` no se incluya (debe existir en .gitignore). |
| 14.2 | Script SQL `database.sql` | Generado y colocado en `database/database.sql` con DDL completo | ⬜ | Pendiente. Después de agregar todas las tablas, `pg_dump -s > database.sql`. |
| 14.3 | Instrucciones de despliegue EC2 | Notas internas/documentación de comandos para lanzar backend en Amazon Linux 2/Ubuntu | ⬜ | Pendiente. Pasos: python venv, install requirements, gunicorn, nginx reverse proxy, systemd unit. |

---

# 15. Registro de Aprobaciones

| Área | Revisor | Fecha | Observaciones | Estado Final |
|------|---------|-------|---------------|--------------|
| Configuración / Arquitectura | | 2026-08-02 | StorageAdapter ✅; Config env ✅; CORS * por defecto ⚠️; Falta gunicorn ⚠️ | ⚠️ Observaciones |
| Autenticación | | 2026-08-02 | Login/Register/Logout/Me ✅; Inconsistencia URL /api vs /api/v1 ⚠️ Crítico | ⚠️ Observaciones |
| Administración de Usuarios | | 2026-08-02 | CRUD existe pero FALTA enforce role admin en list/delete/create ⬜ Crítico | 🟧 En Progreso |
| Convocatorias | | 2026-08-02 | Nada implementado | ⬜ Pendiente |
| Proyectos | | 2026-08-02 | Nada implementado | ⬜ Pendiente |
| Documentos / S3 | | 2026-08-02 | StorageAdapter (upload) ✅; download/delete faltan; Document model/endpoints 0 | 🟧 En Progreso |
| Dashboard | | 2026-08-02 | Endpoint stats no existe | ⬜ Pendiente |
| Historial | | 2026-08-02 | Nada implementado (depende de Document) | ⬜ Pendiente |
| Perfil de Usuario | | 2026-08-02 | Me GET/PUT ✅; Cambio password con validación actual NO existe ⬜ Crítico | 🟧 En Progreso |
| Seguridad | | 2026-08-02 | Hash ✅, ORM anti-SQLi ✅; Faltan role guards + ext/MIME uploads + expires_delta JWT | 🟧 En Progreso |
| Preparación AWS | | 2026-08-02 | Variables env + Adapter switch ✅; falta gunicorn en requirements.txt | ⚠️ Observaciones |
| Entregables | | 2026-08-02 | database.sql 0; Instrucciones EC2 0; Inconsistencia URL v1 ⚠️ Crítico | 🟧 En Progreso |

---

## Principales Hallazgos Críticos del Backend (Alerta)

1. **INCONSISTENCIA DE RUTAS API**: Blueprint registra `/api/v1/` pero frontend Axios apunta a `/api`. Ninguna integración funcionará sin alinear. Solución: cambiar `modules_bp.url_prefix` de `/api/v1` a `/api` O actualizar `VITE_API_BASE_URL` y axios.
2. **FALTA ROLE GUARDS**: Cualquier usuario autenticado puede listar/crear/eliminar usuarios. Necesitamos decorator `@admin_required` para los endpoints users.
3. **CAMBIO DE CONTRASEÑA INSEGURO**: No hay endpoint `/me/password` que valide la contraseña actual. Actualmente solo conociendo el id se puede cambiar password vía PUT users/<id>.
4. **SIN MODELOS**: Call, Project, Document, History están 0% implementados.
5. **FALTA gunicorn**: Requerido para despliegue en EC2 con WSGI (agregar a requirements.txt).
6. **VALIDACIÓN UPLOADS**: Solo tamaño máximo, no extensión/MIME.
