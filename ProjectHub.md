# ProjectHub — Contexto para continuar desarrollo Backend + Frontend

Estoy desarrollando **ProjectHub**, una aplicación web para gestionar convocatorias, proyectos y documentos. El frontend está desarrollado con **Vue 3 + TypeScript + Vite + Pinia + Axios**, y el backend con **Flask + SQLAlchemy + Flask-Migrate + JWT + Flask-CORS**.

La aplicación ya tiene autenticación, usuarios, layout principal y el módulo de convocatorias parcialmente implementado. Ahora necesito continuar con la implementación de los módulos de **Convocatorias (workspace), Proyectos, Documentos e Historial**, manteniendo la arquitectura existente.

---

# 1. Arquitectura actual

## Backend

No existe `backend/src/app.py`.

El punto de entrada de Flask utiliza:

```text
backend/
├── factory.py
├── extensions/
│   ├── cors.py
│   ├── db.py
│   └── jwt.py
└── src/
    ├── config/
    ├── middleware/
    ├── models/
    ├── modules/
    ├── services/
    └── static/
```

La aplicación se crea mediante:

```python
create_app()
```

en `factory.py`.

Actualmente se inicializan:

* SQLAlchemy
* Flask-Migrate
* JWT
* Flask-CORS
* módulos mediante `src.modules.modules_bp`

CORS actualmente utiliza:

```python
resources={r"/api(?:/v1)?/.*": {"origins": allowed_origins}}
```

---

# 2. Autenticación y usuarios existentes

Existe el módulo:

```text
src/modules/users/
```

con:

```text
__init__.py
routes.py
user_controller.py
user_service.py
user_repository.py
```

El frontend tiene:

```text
src/modules/user/services/userService.ts
```

El usuario tiene:

```text
id
username
email
first_name
last_name
role
is_active
profile_picture_url
created_at
```

Roles actuales:

```text
admin
user
```

Existe JWT y el frontend adjunta automáticamente:

```http
Authorization: Bearer <token>
```

mediante:

```text
src/api/axios.ts
```

---

# 3. Frontend actual

Tecnologías:

* Vue 3
* TypeScript
* Vite
* Pinia
* Vue Router
* Axios
* Bootstrap/Tailwind utilities existentes
* Material Symbols

El cliente HTTP está en:

```text
src/api/axios.ts
```

Su `baseURL` es:

```ts
import.meta.env.VITE_API_BASE_URL || '/api'
```

El token JWT se agrega automáticamente mediante interceptor.

---

# 4. Router actual

El router principal está en:

```text
src/router/index.ts
```

Actualmente importa:

```ts
authRoutes
userRoutes
dashboardRoutes
callsRoutes
```

y utiliza `AppLayout.vue` para las rutas privadas.

Se debe extender posteriormente para:

```text
projectsRoutes
documentsRoutes
historyRoutes
```

sin romper las rutas existentes.

---

# 5. AppLayout existente

Archivo:

```text
src/layouts/AppLayout.vue
```

Ya existe navegación lateral y navegación móvil.

Actualmente tiene elementos para:

```text
Dashboard
Usuarios
Convocatorias
Mis proyectos
Mis documentos
Historial
Configuración
```

Pero varios elementos todavía apuntan incorrectamente a:

```text
dashboard
```

Por ejemplo:

```ts
{ key: 'projects', icon: 'folder', title: 'Mis proyectos', routeName: 'dashboard' }
{ key: 'documents', icon: 'description', title: 'Mis documentos', routeName: 'dashboard' }
{ key: 'history', icon: 'history', title: 'Historial', routeName: 'dashboard' }
```

Esto debe corregirse cuando existan las nuevas rutas.

---

# 6. Módulo de Convocatorias — BACKEND EXISTENTE

Existe:

```text
src/modules/calls/
├── call_repository.py
├── call_service.py
├── call_controller.py
└── routes.py
```

Modelos:

```text
src/models/call.py
src/models/call_requirement.py
src/models/call_participant.py
```

## Modelo Call

Tabla:

```text
calls
```

Campos principales:

```text
id
title
description
start_date
end_date
is_active
created_at
updated_at
```

Relaciones:

```text
Call
 ├── requirements
 └── participants
```

## CallRequirement

Tabla:

```text
call_requirements
```

Campos:

```text
id
call_id
title
description
is_required
created_at
```

## CallParticipant

Tabla:

```text
call_participants
```

Campos:

```text
id
call_id
user_id
status
joined_at
```

---

# 7. Endpoints actuales de Convocatorias

Backend:

```http
GET    /calls/
GET    /calls/<id>
GET    /calls/<id>/workspace
POST   /calls/
PUT    /calls/<id>
DELETE /calls/<id>
```

Permisos:

```text
GET → usuario autenticado
POST → admin
PUT → admin
DELETE → admin
workspace → usuario autenticado
```

El endpoint importante para continuar es:

```http
GET /calls/<id>/workspace
```

Actualmente devuelve:

```json
{
  "data": {
    "call": {},
    "requirements": [],
    "project": null,
    "documents": [],
    "tracking": [],
    "stats": {
      "documents_uploaded": 0,
      "progress": 0
    }
  }
}
```

Esto actualmente es solamente una estructura inicial.

---

# 8. PROBLEMA ACTUAL DEL WORKSPACE

El frontend necesita implementar el workspace de una convocatoria.

Archivos que todavía están vacíos y deben desarrollarse:

```text
src/modules/calls/workspace/CallProject.vue
src/modules/calls/workspace/CallTracking.vue
src/modules/calls/workspace/CallDocuments.vue
src/modules/calls/routes/index.ts
```

La idea del workspace es que una convocatoria pueda mostrar:

```text
Convocatoria
│
├── Información de convocatoria
│
├── Requisitos
│
├── Proyecto asociado
│
├── Documentos
│
├── Seguimiento
│
└── Estadísticas/progreso
```

Hay que decidir e implementar correctamente la integración entre estas secciones y los módulos de proyectos/documentos.

---

# 9. Módulo PROYECTOS — NO EXISTE EN BACKEND

Actualmente NO existe:

```text
src/modules/projects/
```

en backend.

Por lo tanto, antes de intentar hacer únicamente el frontend, se debe crear el módulo completo.

Debe seguir la arquitectura:

```text
routes
→ controller
→ service
→ repository
→ model
```

Se necesita determinar e implementar:

```text
src/models/project.py

src/modules/projects/
├── __init__.py
├── routes.py
├── project_controller.py
├── project_service.py
└── project_repository.py
```

También deberá agregarse el modelo a:

```text
src/models/__init__.py
```

y posteriormente crear la migración correspondiente.

---

# 10. Funcionalidad esperada de PROYECTOS

El módulo debe permitir gestionar proyectos relacionados con convocatorias y usuarios.

Como mínimo debe contemplar:

```text
Crear proyecto
Consultar proyectos
Consultar proyecto por ID
Actualizar proyecto
Eliminar proyecto
```

Y debería existir relación con:

```text
User
Call
Documents
```

La estructura exacta de campos debe definirse antes de implementar para evitar crear un modelo incompatible con el frontend.

El objetivo funcional es que un usuario pueda tener proyectos asociados a convocatorias.

---

# 11. Archivos FRONTEND de PROYECTOS

Actualmente están vacíos y deben crearse:

```text
src/modules/projects/services/projectService.ts

src/modules/projects/views/ProjectsListView.vue
src/modules/projects/views/ProjectDetailView.vue

src/modules/projects/components/ProjectCard.vue
src/modules/projects/components/ProjectFilter.vue

src/modules/projects/routes/index.ts
```

Responsabilidad de cada uno:

### projectService.ts

Centralizar las llamadas Axios al backend:

```text
GET proyectos
GET proyecto por ID
POST proyecto
PUT proyecto
DELETE proyecto
```

### ProjectsListView.vue

Mostrar:

```text
Lista de proyectos
Filtros
Estados
Acciones
```

### ProjectDetailView.vue

Mostrar el detalle completo de un proyecto y su relación con:

```text
convocatoria
documentos
progreso
```

### ProjectCard.vue

Componente reutilizable para representar un proyecto.

### ProjectFilter.vue

Filtros para la lista de proyectos.

### routes/index.ts

Definir rutas como:

```text
/projects
/projects/:id
```

con nombres consistentes, por ejemplo:

```text
projects-list
project-detail
```

---

# 12. Módulo DOCUMENTOS — NO EXISTE EN BACKEND

Actualmente NO existe:

```text
src/modules/documents/
```

en backend.

Debe crearse un módulo completo para manejar documentos.

Debe seguir:

```text
routes
→ controller
→ service
→ repository
→ model
→ StorageService
```

Ya existe un servicio de almacenamiento:

```text
src/services/storage_service.py
```

Este servicio ya está pensado para soportar almacenamiento local/S3.

Hay que reutilizarlo en lugar de crear otro sistema de almacenamiento.

---

# 13. Funcionalidad esperada de DOCUMENTOS

Los documentos deben poder:

```text
Subirse
Listarse
Consultar información
Descargarse
Eliminarse
```

Y deben estar relacionados con:

```text
User
Project
Call
```

El sistema debe guardar metadatos, por ejemplo:

```text
id
project_id
user_id
filename
original_filename
file_path / storage_key
mime_type
size
created_at
```

La estructura definitiva debe definirse antes de crear el modelo.

---

# 14. FRONTEND de DOCUMENTOS

Archivos que deben crearse:

```text
src/modules/documents/services/documentService.ts

src/modules/documents/views/DocumentsView.vue

src/modules/documents/components/DocumentTable.vue

src/modules/documents/routes/index.ts
```

### documentService.ts

Debe centralizar:

```text
listar documentos
subir documento
descargar documento
eliminar documento
```

Debe soportar `FormData` para uploads.

### DocumentsView.vue

Vista principal para:

```text
documentos del usuario
subida de archivos
filtros
eliminación
descarga
```

### DocumentTable.vue

Tabla reutilizable con:

```text
Nombre
Proyecto
Tipo
Tamaño
Fecha
Acciones
```

### routes/index.ts

Ruta esperada:

```text
/documents
```

por ejemplo:

```text
documents-list
```

---

# 15. Módulo HISTORIAL — NO EXISTE

No existe todavía backend para historial.

En frontend están vacíos:

```text
src/modules/history/views/HistoryView.vue
src/modules/history/routes/index.ts
```

El historial debe mostrar acciones importantes realizadas en el sistema, por ejemplo:

```text
Proyecto creado
Proyecto actualizado
Documento subido
Documento eliminado
Convocatoria registrada
Cambio de estado
```

Se debe decidir si se implementará como:

```text
activity log / audit log
```

con un modelo tipo:

```text
id
user_id
action
entity_type
entity_id
description
created_at
```

El backend deberá exponer un endpoint para consultar el historial.

---

# 16. Integración final esperada

La arquitectura funcional debería terminar aproximadamente así:

```text
                    ┌──────────────┐
                    │ Convocatoria │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Proyecto   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │Documentos│ │Seguimiento│ │Historial │
        └──────────┘ └──────────┘ └──────────┘
```

Relaciones principales:

```text
User
 │
 ├── Projects
 │
 ├── Documents
 │
 └── History

Call
 │
 ├── Requirements
 ├── Participants
 └── Projects

Project
 │
 ├── Documents
 └── Tracking
```

---

# 17. Orden recomendado de implementación

NO empezar creando todos los componentes Vue de golpe.

El orden recomendado es:

### FASE 1 — Modelado backend

Definir:

```text
Project
Document
History/Activity
```

y sus relaciones.

### FASE 2 — Migraciones

Crear migraciones Flask-Migrate.

Verificar que la base de datos tenga correctamente las nuevas tablas y foreign keys.

### FASE 3 — Backend Projects

Implementar:

```text
repository
service
controller
routes
```

y probar API.

### FASE 4 — Backend Documents

Implementar:

```text
model
repository
service
controller
routes
```

integrando `StorageService`.

### FASE 5 — Backend History

Implementar:

```text
model
repository
service
controller
routes
```

### FASE 6 — Workspace Calls

Completar:

```text
GET /calls/<id>/workspace
```

para que realmente devuelva:

```text
call
requirements
project
documents
tracking
stats
```

en lugar de valores vacíos.

### FASE 7 — Frontend Projects

Crear:

```text
projectService.ts
ProjectsListView.vue
ProjectDetailView.vue
ProjectCard.vue
ProjectFilter.vue
routes/index.ts
```

### FASE 8 — Frontend Documents

Crear:

```text
documentService.ts
DocumentsView.vue
DocumentTable.vue
routes/index.ts
```

### FASE 9 — Frontend History

Crear:

```text
HistoryView.vue
routes/index.ts
```

### FASE 10 — Integración Router/AppLayout

Actualizar:

```text
src/router/index.ts
src/layouts/AppLayout.vue
```

para que:

```text
Mis proyectos → /projects
Mis documentos → /documents
Historial → /history
Convocatorias → /calls
```

ya no apunten a `dashboard`.

---

# 18. Importante antes de escribir código

Antes de generar archivos completos, revisar primero los archivos existentes que puedan afectar las relaciones:

```text
src/models/user.py
src/models/base.py
src/models/__init__.py

src/services/storage_service.py

src/modules/__init__.py

src/modules/calls/__init__.py
src/modules/calls/routes.py

src/config/default.py

frontend:
src/modules/calls/
src/modules/dashboard/
src/modules/user/
src/stores/authStore.ts
src/api/axios.ts
```

También revisar cómo se registra actualmente:

```python
modules_bp
```

para no crear blueprints que nunca se registren.

---

# 19. Objetivo de esta continuación

Quiero continuar el desarrollo de ProjectHub de manera ordenada.

La prioridad es:

```text
BACKEND
  ↓
Modelos y relaciones
  ↓
Migraciones
  ↓
Projects API
  ↓
Documents API
  ↓
History API
  ↓
Call Workspace API
  ↓
FRONTEND
  ↓
Projects
  ↓
Documents
  ↓
History
  ↓
Calls Workspace
  ↓
Router + navegación
  ↓
Pruebas e integración
```

No asumir que los módulos `projects` y `documents` ya existen en backend: **actualmente no existen y deben construirse desde cero**.

Tampoco asumir que `app.py` existe: **el proyecto utiliza `factory.py` con `create_app()`**.

La implementación debe respetar la arquitectura y convenciones que ya existen en ProjectHub y evitar reemplazar código funcional existente innecesariamente.
