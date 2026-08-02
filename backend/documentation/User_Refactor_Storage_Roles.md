# Refactorización: Modelo de Usuario, Roles y Estrategia de Almacenamiento Local/S3

**Fecha:** 2026-08-01
**Versión:** 1.0
**Autor:** Arquitectura de Software

---

## 1. Resumen de Cambios

Esta refactorización introduce cuatro capacidades principales al backend:

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | `StorageService` | Servicio unificado con patrón Adapter para alternar entre almacenamiento Local y AWS S3 |
| 2 | `User` Model | Extensión de la entidad User con campos de perfil (first_name, last_name), roles (user/admin) y foto de perfil |
| 3 | Auth + User Services | Actualización de servicios para soportar nuevos campos, control de roles y upload de archivos |
| 4 | Controllers + Routes | Soporte para `multipart/form-data` y JSON, nuevo endpoint `PUT /api/auth/me` |

---

## 2. Patrón Adapter para Almacenamiento

### 2.1. Estructura

```
StorageService (Facade)
    ├── StorageAdapter (Abstract)
    ├── LocalStorageAdapter
    └── S3StorageAdapter
```

### 2.2. Archivo: `src/services/storage_service.py`

#### Clases Principales

**StorageAdapter (ABC):**
- Define la interfaz `upload_file(file_storage, folder) -> str`

**LocalStorageAdapter:**
- Guarda archivos en `src/static/uploads/<folder>/`
- Nombre de archivo: `{uuid}_{nombre_original}`
- Retorna ruta relativa: `/static/uploads/<folder>/<filename>`

**S3StorageAdapter:**
- Utiliza `boto3` para subir archivos al bucket configurado
- ACL: `public-read`
- Retorna URL pública: `https://<bucket>.s3.<region>.amazonaws.com/<folder>/<filename>`

**StorageService:**
- Singleton lazy-loaded (`_adapter`)
- Lee `STORAGE_PROVIDER` del entorno: `local` (default) o `s3`

### 2.3. Variables de Entorno Requeridas

| Variable | Valor Default | Descripción |
|----------|--------------|-------------|
| `STORAGE_PROVIDER` | `local` | `local` o `s3` |
| `AWS_ACCESS_KEY_ID` | - | Access Key de AWS (para S3) |
| `AWS_SECRET_ACCESS_KEY` | - | Secret Key de AWS (para S3) |
| `AWS_REGION` | `us-east-1` | Región AWS |
| `S3_BUCKET_NAME` | `your-s3-bucket-name` | Nombre del bucket S3 |

---

## 3. Modelo de Usuario Extendido

### 3.1. Archivo: `src/models/user.py`

#### Nuevos Campos

| Campo | Tipo | Nullable | Default | Descripción |
|-------|------|----------|---------|-------------|
| `first_name` | `String(80)` | Sí | `None` | Nombre del usuario |
| `last_name` | `String(80)` | Sí | `None` | Apellido del usuario |
| `role` | `String(20)` | **No** | `'user'` | `'user'` o `'admin'` |
| `profile_picture_url` | `String(255)` | Sí | `None` | URL de la foto de perfil |

#### Método `to_dict()` Actualizado

```python
{
    'id': int,
    'username': str,
    'email': str,
    'first_name': str | None,
    'last_name': str | None,
    'role': str,              # 'user' | 'admin'
    'profile_picture_url': str | None,
    'is_active': bool,
    'created_at': str (ISO 8601)
}
```

### 3.2. Migración de Base de Datos

Para aplicar los cambios en la BD se requiere generar y ejecutar una migración:

```powershell
cd backend
python run.py db migrate -m "add_user_profile_and_role_fields"
python run.py db upgrade
```

---

## 4. Capa de Servicios

### 4.1. `AuthService` (`src/modules/auth/auth_service.py`)

#### `register_user(username, email, password, first_name=None, last_name=None)`

- **Rol:** Asigna automáticamente `role='user'`
- **Campos Aceptados:** `username`, `email`, `password`, `first_name`, `last_name`
- **Validaciones:**
  - Email único
  - Username único
- **Retorna:** Objeto `User` persistido

---

### 4.2. `UserService` (`src/modules/users/user_service.py`)

#### `create_user(username, email, password, first_name=None, last_name=None, role='user')`

- **Uso:** Creación de usuarios por administradores
- **Campos Aceptados:** Además de los de registro, acepta `role`
- **Validaciones:**
  - Email único
  - Username único
  - Rol válido (`'user'` o `'admin'`)
- **Retorna:** `dict` del usuario

---

#### `update_user(user_id, data, file=None, is_admin=False)`

**Parámetros:**
- `user_id`: ID del usuario a actualizar
- `data`: `dict` con campos opcionales a actualizar
- `file`: `FileStorage` (imagen de perfil opcional)
- `is_admin`: `bool` indica si el solicitante tiene privilegios de admin

**Campos Actualizables:**

| Campo | Permiso | Notas |
|-------|---------|-------|
| `username` | Todos | Único |
| `email` | Todos | Único |
| `first_name` | Todos | - |
| `last_name` | Todos | - |
| `password` | Todos | Hasheado |
| `is_active` | Todos | `bool` |
| `role` | **Solo Admin** | `'user'` o `'admin'` |
| `profile_picture_url` | Todos | Si se envía `file`, se sube a través de `StorageService` en carpeta `profiles` |

**Errores:**
- `ValueError`: Usuario no encontrado, datos inválidos
- `PermissionError`: Intento de modificar `role` sin ser admin

---

## 5. Capa de Controladores

### 5.1. Estrategia de Extracción de Datos

Ambos controladores (`AuthController` y `UserController`) incluyen el método helper `_extract_data()` que:

1. Intenta parsear `request.get_json(silent=True)` (application/json)
2. Luego parsea `request.form.to_dict()` (multipart/form-data, application/x-www-form-urlencoded)
3. Hace merge de ambos, dando prioridad al formulario si hay colisiones

Esto permite que los endpoints acepten ambos formatos de forma transparente.

---

### 5.2. `AuthController` (`src/modules/auth/auth_controller.py`)

#### Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/register` | No | Registro público (rol = user) |
| POST | `/login` | No | Autenticación |
| POST | `/refresh` | Refresh Token | Renovar access token |
| POST | `/logout` | JWT | Cerrar sesión |
| GET | `/me` | JWT | Obtener perfil actual |
| **PUT** | **`/me`** | **JWT** | **Actualizar perfil actual (incluye foto)** |

#### Nuevo: `update_current_user()` (PUT /me)

- Actualiza el perfil del usuario autenticado
- Acepta `multipart/form-data` con archivo de imagen en el campo `file`
- Internamente llama a `UserService.update_user` con `is_admin=False`

---

### 5.3. `UserController` (`src/modules/users/user_controller.py`)

#### Métodos Helper Nuevos

- **`_is_admin()`:** Verifica si el usuario del JWT actual tiene `role == 'admin'`
- Consulta `UserRepository` con `get_jwt_identity()`

#### Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/users` | JWT | Listar todos los usuarios |
| GET | `/users/<id>` | JWT | Obtener usuario por ID |
| POST | `/users` | JWT | Crear usuario (admin: puede asignar role) |
| PUT | `/users/<id>` | JWT | Actualizar usuario (con archivo; role solo por admin) |
| DELETE | `/users/<id>` | JWT | Eliminar usuario |

---

## 6. Capa de Rutas

### 6.1. `src/modules/auth/routes.py`

```python
@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    return AuthController.update_current_user()
```

**Mantenimiento de `@jwt_required()`:**
- Todas las rutas protegidas mantienen su decorador
- `/refresh` usa `@jwt_required(refresh=True)`
- Nuevas rutas (`PUT /me`) incluyen protección JWT

### 6.2. `src/modules/users/routes.py`

Sin cambios en las rutas; los controladores actualizados soportan los nuevos formatos.

---

## 7. Configuración y Servicio de Archivos Estáticos

### 7.1. `src/config/default.py`

Adiciones:
```python
STORAGE_PROVIDER = os.getenv('STORAGE_PROVIDER', 'local')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB límite de upload
```

### 7.2. `factory.py`

- `static_folder`: Ahora apunta a `backend/src/static`
- `static_url_path`: `/static`
- Crea automáticamente `src/static/uploads/` si no existe
- Ruta explícita `GET /static/uploads/<folder>/<filename>` para servir archivos subidos

---

## 8. Ejemplos de Uso

### 8.1. Registro Público (JSON)

```http
POST /api/auth/register
Content-Type: application/json

{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
}
```

### 8.2. Actualizar Perfil con Foto (multipart/form-data)

```http
PUT /api/auth/me
Authorization: Bearer <JWT>
Content-Type: multipart/form-data

first_name: "Juan"
last_name: "Pérez"
file: <binary-image> (campo: "file")
```

### 8.3. Admin Crear Usuario Admin

```http
POST /api/users
Authorization: Bearer <admin-jwt>
Content-Type: application/json

{
    "username": "superadmin",
    "email": "admin@projecthub.com",
    "password": "adminpass123",
    "first_name": "System",
    "last_name": "Admin",
    "role": "admin"
}
```

### 8.4. Admin Cambiar Rol de Usuario

```http
PUT /api/users/5
Authorization: Bearer <admin-jwt>
Content-Type: application/json

{
    "role": "admin"
}
```

---

## 9. Matriz de Cumplimiento

| Requisito | Archivo | Cumplido |
|-----------|---------|:--------:|
| StorageService Adapter Local/S3 | `storage_service.py` | ✅ |
| UUID + nombre original en uploads | `storage_service.py` | ✅ |
| S3 con boto3 y URL pública | `storage_service.py` | ✅ |
| STORAGE_PROVIDER env var | `default.py` + `storage_service.py` | ✅ |
| User: first_name | `user.py` | ✅ |
| User: last_name | `user.py` | ✅ |
| User: role (user/admin default user) | `user.py` | ✅ |
| User: profile_picture_url | `user.py` | ✅ |
| to_dict() incluye nuevos campos | `user.py` | ✅ |
| Register acepta first/last name | `auth_service.py` | ✅ |
| Register asigna role=user | `auth_service.py` | ✅ |
| UserService.create_user con role | `user_service.py` | ✅ |
| update_user recibe file | `user_service.py` | ✅ |
| StorageService.upload_file(folder='profiles') | `user_service.py` | ✅ |
| update_user actualiza profile_picture_url | `user_service.py` | ✅ |
| Actualización first/last/password/is_active | `user_service.py` | ✅ |
| Actualización role solo por admin | `user_service.py` | ✅ |
| Controladores: JSON + form data | `auth_controller.py`, `user_controller.py` | ✅ |
| @jwt_required() mantenido | `routes.py` (ambos) | ✅ |
| PUT /me endpoint | `auth_routes.py` + `auth_controller.py` | ✅ |
| 4 capas: Routes → Controller → Service → Repository | Todos los módulos | ✅ |

---

## 10. Siguientes Pasos

1. **Generar migración de BD:** Aplicar los cambios del modelo User
2. **Crear archivo `.env.example`:** Documentar las nuevas variables `STORAGE_PROVIDER` y AWS
3. **Pruebas de integración:** Validar endpoints con y sin archivos
4. **Políticas AWS IAM:** Configurar bucket S3 con políticas CORS y usuario IAM limitado
