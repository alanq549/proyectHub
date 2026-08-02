# Seed Progresivo de ProjectHub por Endpoints (Python)

**Fecha:** 2026-08-01
**Versión:** 2.0 (Python, sin dependencias externas)
**Ubicación:** `backend/seed/`

---

## 1. ¿Por qué Seed por Endpoints y por qué Python?

| Motivo | Detalle |
|--------|---------|
| **Contratos de API consistentes** | El seed ejercita los mismos endpoints que el frontend → detecta desviaciones |
| **Password hashing** | Nunca SQL directo; pasa por `User.set_password()` (werkzeug hash) |
| **Reglas de negocio** | Validaciones de email/username único, roles, campos nulos se ejecutan igual que en producción |
| **EC2-friendly** | Ejecutable en instancias Linux EC2 sin instalar Node.js, ni npm. Usa la misma runtime Python del backend. |
| **Cero dependencias externas** | Usa `urllib` y `json` de la librería estándar; no requiere `pip install requests`. |

---

## 2. Ubicación y Estructura

```
backend/
├── seed/
│   ├── __init__.py
│   ├── run_seed.py              ← entry point (python run_seed.py)
│   ├── config.py                ← env vars PROJECTHUB_*
│   ├── lib/
│   │   ├── __init__.py
│   │   ├── http_client.py       ← request(), expect(), build_url(), multipart stdlib
│   │   └── auth.py              ← ensure_admin(), login(), register_public_user()
│   ├── data/
│   │   ├── __init__.py
│   │   └── users.py             ← 5 usuarios demo iniciales
│   └── seeds/
│       ├── __init__.py
│       └── users.py             ← seed_users(admin_token)
```

---

## 3. Avatar por Defecto (`icon_default.png`)

### 3.1. Ubicación

Se movió desde `src/static/uploads/icon_default.png` → **`src/static/defaults/icon_default.png`**.

**Por qué no `uploads/`:**
- `uploads/` = archivos generados por usuarios vía `StorageService`.
- `defaults/` = assets estáticos del sistema, versionados con el código.

**Por qué no una carpeta `/public`:**
- Flask ya usa nativamente `/static/`; el frontend usa `/public` → mantener separación de concerns.

### 3.2. Mecanismos de Aplicación

**En `src/models/user.py`:**

```python
DEFAULT_PROFILE_PICTURE_URL = '/static/defaults/icon_default.png'

class User(db.Model):
    profile_picture_url = db.Column(
        db.String(255),
        default=DEFAULT_PROFILE_PICTURE_URL,   # al INSERT si no se envía
        nullable=True
    )

    def to_dict(self):
        return {
            ...
            'profile_picture_url': (
                self.profile_picture_url
                or DEFAULT_PROFILE_PICTURE_URL   # fallback si columna es NULL
            ),
            ...
        }
```

**Rutas servidas por `factory.py`:**
```
GET /static/<path:filename>
GET /static/defaults/<path:filename>
GET /static/uploads/<folder>/<filename>
```

---

## 4. Bootstrap del Primer Administrador

El registro público siempre crea `role='user'`, pero necesitamos un admin con JWT.

**Solución en `AuthService.register_user()`:**

```
SI  User.query.count() == 0
AND BOOTSTRAP_FIRST_USER_AS_ADMIN == 'true' (default true)
=> EL PRIMER registro recibe role='admin'

En cualquier otro caso => role='user' (registro público normal).
```

| Variable | Default | Descripción |
|----------|---------|-------------|
| `BOOTSTRAP_FIRST_USER_AS_ADMIN` | `true` | Solo el primer registro es promovido a admin |
| `PROJECTHUB_API_URL` | `http://localhost:5000/api/v1` | Base URL del backend (para el seed) |
| `PROJECTHUB_ADMIN_EMAIL` | `admin@projecthub.local` | Credencial del admin que crea el seed |
| `PROJECTHUB_ADMIN_PASSWORD` | `Admin1234!` | Credencial del admin (viaja por API → hasheado al llegar al backend) |
| `PROJECTHUB_ADMIN_USERNAME` | `admin` | Username del admin |
| `PROJECTHUB_ADMIN_FIRSTNAME` | `System` | Nombre |
| `PROJECTHUB_ADMIN_LASTNAME` | `Administrator` | Apellido |

**Seguridad Producción (EC2):**
- Después de la primera ejecución del seed → setear `BOOTSTRAP_FIRST_USER_AS_ADMIN=false`.
- Rotar el password del admin desde el endpoint `PUT /users/:id`.

---

## 5. Datos Inyectados (Usuarios)

### 5.1. Admin seed

| Campo | Valor |
|-------|-------|
| username | `admin` |
| email | `admin@projecthub.local` |
| password | `Admin1234!` (hasheado por werkzeug al ejecutar el endpoint `/auth/register` o `/users`) |
| first_name | `System` |
| last_name | `Administrator` |
| role | `admin` (SOLO si es el primer usuario de la tabla) |
| profile_picture_url | `/static/defaults/icon_default.png` |

### 5.2. Usuarios Demo (5 usuarios `role=user`)

| username | email | password | first_name | last_name |
|----------|-------|----------|------------|-----------|
| `ana.lopez` | `ana.lopez@projecthub.local` | `Ana1234!` | Ana | López |
| `carlos.gomez` | `carlos.gomez@projecthub.local` | `Carlos1234!` | Carlos | Gómez |
| `maria.ramirez` | `maria.ramirez@projecthub.local` | `Maria1234!` | María | Ramírez |
| `pedro.martinez` | `pedro.martinez@projecthub.local` | `Pedro1234!` | Pedro | Martínez |
| `laura.torres` | `laura.torres@projecthub.local` | `Laura1234!` | Laura | Torres |

Todos creados via `POST /api/v1/users` autenticados como admin → password viaja por JSON al endpoint, backend aplica `User.set_password()` → **hash werkzeug en la BD**.

**Idempotencia:**
- Si el usuario ya existe (buscado por email), no se duplica.
- Si `role`, `first_name` o `last_name` difieren de `data/users.py`, el seed converge los datos usando `PUT /users/:id`.
- El módulo `seed_users` valida además que los usuarios recién creados usen `DEFAULT_PROFILE_PICTURE_URL`.

---

## 6. Endpoints Ejercitados

| # | Método | Ruta | Propósito |
|---|--------|------|-----------|
| 1 | POST | `/auth/login` | Obtener access_token del admin |
| 2 | GET | `/auth/me` | Verificar role del admin logueado |
| 3 | POST | `/auth/register` | Crear el admin inicial si la tabla está vacía (usa bootstrap first-user) |
| 4 | GET | `/users` | Listar usuarios y buscar por email (idempotencia) |
| 5 | POST | `/users` | Crear cada usuario demo como admin → werkzeug hash |
| 6 | PUT | `/users/:id` | Alinear role / first_name / last_name si existían antes |

---

## 7. Ejecución (Local o EC2)

**Requisito:** Python 3.10+ (misma runtime del backend). **Sin dependencias externas**, sin `pip install`.

```bash
# 1. Levantar el backend
cd backend
python run.py runserver -h 0.0.0.0 -p 5000

# 2. Ejecutar el seed (otra terminal o SSH en EC2)
cd backend
python seed/run_seed.py

# 3. Con variables personalizadas (EC2)
export PROJECTHUB_API_URL="http://127.0.0.1:5000/api/v1"
export PROJECTHUB_ADMIN_PASSWORD='S3cr3t4dm1n!'
export BOOTSTRAP_FIRST_USER_AS_ADMIN=true
python seed/run_seed.py
```

**PowerShell (Windows):**
```powershell
cd backend
$env:PROJECTHUB_ADMIN_PASSWORD = "SuperAdmin999!"
python seed/run_seed.py
```

**Salida esperada:**
```
╔══════════════════════════════════════════════════════════════╗
║  PROJECTHUB · SEED PROGRESIVO POR ENDPOINTS (PYTHON)        ║
╚══════════════════════════════════════════════════════════════╝

> Asegurando usuario administrador (por endpoints)...
> Seed del módulo Users (admin crea/actualiza 5 usuarios demo)...
  Creados:
    - #2 ana.lopez@projecthub.local (user) · avatar=/static/defaults/icon_default.png
    ...

── RESUMEN DE SEED ──────────────────────────────────────────
[AUTH] 1 paso(s):
  • ensureAdmin ................................................ → CREADO

[USERS] 1 paso(s):
  • seedUsers .................................................. → OK

─────────────────────────────────────────────────────────────
✅ Seed completado satisfactoriamente.
```

---

## 8. Cómo Añadir Módulos Futuros

Cuando existan endpoints de otros dominios (Projects, Tasks, Teams, etc.):

1. **Datos demo** → `backend/seed/data/<module>.py` con `DATOS = [ {...}, ... ]`
2. **Seed** → `backend/seed/seeds/<module>.py`
   ```python
   from ..lib.http_client import request, expect

   def seed_<module>(admin_token, ctx=None):
       ctx = ctx or {}
       # 1. Buscar existentes por clave única
       # 2. Crear faltantes por POST /endpoint (token=admin_token)
       # 3. Actualizar desalineados por PUT /endpoint/:id
       # 4. expect(200|201, res, "contexto") para validar
       return { "created": [...], "skipped": [...], ... }
   ```
3. **Integrar** → en `run_seed.py`:
   ```python
   from seed.seeds.<module> import seed_<module>
   # ... después de seed_users
   report = seed_<module>(admin["token"])
   record("<MODULE>", "seed<Module>", f"creados={len(report['created'])}...", "OK")
   ```
4. **Idempotente siempre**: buscar antes de crear.
5. **Sin dependencias externas**: seguir usando `request()` de `lib/http_client.py` (urllib estándar).

---

## 9. Checklist de Cumplimiento

| Requisito | Cumplido |
|-----------|:--------:|
| Seed 100% Python, sin Node.js / npm / axios | ✅ |
| Seed sin dependencias externas (stdlib urllib + json) | ✅ |
| Seed por endpoints HTTP, no SQL directo | ✅ |
| Passwords viajan por API → `set_password()` werkzeug hash | ✅ |
| Nunca contraseña texto plano en BD | ✅ |
| Registro público NO pide role ni profile_picture | ✅ |
| `icon_default.png` = fallback universal (default de columna + fallback to_dict) | ✅ |
| Avatar default en `static/defaults/` (no mezclar con uploads de usuarios) | ✅ |
| Rutas estáticas servidas por Flask | ✅ |
| Seed idempotente | ✅ |
| Admin inicial via endpoints (bootstrap first-user = admin) | ✅ |
| Estructura extensible módulo-a-módulo | ✅ |
| Ejecutable directamente en EC2 con el Python del backend | ✅ |
| Documentación actualizada a Python | ✅ |
