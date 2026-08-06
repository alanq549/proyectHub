# Sistema Web de Gestión de Convocatorias y Proyectos

## 1. Descripción general

El proyecto consiste en el desarrollo de una aplicación web orientada a la gestión de usuarios, convocatorias, proyectos y documentos asociados.

La solución estará basada en una arquitectura cliente-servidor, separando la capa de presentación, lógica de negocio, almacenamiento de información y gestión de archivos.

El sistema estará compuesto por:

- **Frontend:** desarrollado con Vue.js utilizando Bootstrap 5 y/o tailwindcss para la construcción de la interfaz gráfica.
- **Backend:** desarrollado mediante una API REST utilizando Flask como framework principal.
- **Base de datos:** PostgreSQL para el almacenamiento estructurado de la información.
- **Almacenamiento de archivos:** Amazon S3 como servicio destinado al manejo de documentos y archivos multimedia.
- **Infraestructura:** Amazon EC2 como servicio de despliegue de la aplicación.
- **Seguridad y permisos:** AWS IAM para la administración de accesos y permisos sobre los recursos utilizados.

El desarrollo será realizado inicialmente en un ambiente local, permitiendo la construcción, pruebas y validación del sistema. Posteriormente, la arquitectura permitirá la migración hacia infraestructura AWS sin requerir cambios importantes en la lógica principal de la aplicación.

---

# 2. Alcance del sistema

El sistema tiene como objetivo proporcionar una plataforma web para la administración de usuarios, convocatorias, proyectos y documentos asociados.

La aplicación permitirá:

- Gestionar usuarios con diferentes niveles de acceso.
- Administrar convocatorias dentro del sistema.
- Registrar y administrar proyectos.
- Gestionar documentos asociados a proyectos y usuarios.
- Consultar información estadística general mediante un dashboard.
- Mantener un historial de acciones relacionadas con documentos.
- Permitir a los usuarios modificar su información personal.

La solución será desarrollada bajo una arquitectura escalable, preparada para funcionar tanto en un ambiente local de desarrollo como en un ambiente productivo utilizando servicios de Amazon Web Services.

---

# 3. Arquitectura del sistema

La arquitectura propuesta sigue un modelo cliente-servidor con separación de responsabilidades.

                Usuario
                   |
                   |
            Navegador Web
                   |
                   |
         Vue.js + Bootstrap 5/ tailwindcss
                   |
                   |
          API REST Flask
                   |
    --------------------------------
    |              |               |
    |              |               |
PostgreSQL     Almacenamiento    AWS IAM
  (Datos)       de Archivos      (Permisos)
             (Local / S3)

---

# 3.1 Frontend

El frontend será responsable de la interacción con el usuario y la presentación de información.

Responsabilidades:

- Construcción de interfaces gráficas.
- Navegación entre módulos.
- Validación de formularios.
- Consumo de servicios REST.
- Manejo de sesión del usuario.
- Visualización de información estadística.
- Gestión de archivos enviados o consultados.

Tecnologías utilizadas:

- Vue.js
- Bootstrap 5
- HTML5
- CSS3
- JavaScript / TypeScript

---

# 3.2 Backend

El backend funcionará como una API REST encargada de procesar solicitudes provenientes del frontend.

Responsabilidades:

- Implementación de endpoints REST.
- Gestión de autenticación.
- Control de usuarios.
- Administración de permisos.
- Procesamiento de reglas del negocio.
- Comunicación con PostgreSQL.
- Gestión de archivos mediante Amazon S3.

Tecnologías utilizadas:

- Python
- Flask
- Flask REST API
- PostgreSQL
- Librerías de integración con AWS

---

# 3.3 Base de datos PostgreSQL

PostgreSQL será utilizado como sistema principal de almacenamiento estructurado.

La base de datos almacenará información relacionada con:

- Usuarios.
- Roles.
- Convocatorias.
- Proyectos.
- Documentos registrados.
- Historial de cargas.
- Información del perfil del usuario.

El proyecto incluirá un archivo SQL encargado de la creación de la estructura necesaria de la base de datos.

---

# 3.4 Amazon S3

Amazon S3 será utilizado como servicio de almacenamiento externo para archivos.

Será utilizado para almacenar:

- Documentos asociados a proyectos.
- Archivos cargados por usuarios.
- Fotografías de perfil.

El sistema permitirá:

- Carga de archivos.
- Consulta de archivos registrados.
- Descarga de documentos.
- Asociación entre archivos y registros almacenados en PostgreSQL.

La base de datos almacenará la información descriptiva del archivo, mientras que Amazon S3 almacenará físicamente el recurso.

---

# 3.5 Amazon EC2

Amazon EC2 será utilizado como plataforma de despliegue de la aplicación.

La arquitectura contempla la posibilidad de ejecutar:

- Backend Flask.
- Servicios necesarios para la aplicación.
- Aplicación web disponible mediante acceso público.

La configuración de infraestructura será realizada durante la etapa de despliegue del sistema.

---

# 3.6 AWS IAM

AWS IAM será utilizado para administrar la seguridad y permisos sobre los recursos utilizados.

Permitirá gestionar:

- Usuarios y roles de AWS.
- Permisos de acceso.
- Restricciones sobre servicios como EC2 y S3.
- Control seguro de operaciones realizadas por la aplicación.

---

# 4. Manejo de ambientes

El sistema estará preparado para trabajar con diferentes ambientes mediante configuraciones externas.

## Ambiente local

Utilizado durante la etapa de desarrollo y pruebas.

Componentes:

- Frontend Vue.js ejecutándose localmente.
- Backend Flask como API REST local.
- Base de datos PostgreSQL local.
- Configuración de almacenamiento adaptable.

Objetivos:

- Desarrollo de funcionalidades.
- Pruebas de integración.
- Validación del funcionamiento completo.

---

## Ambiente productivo

Preparado para ejecutarse utilizando infraestructura AWS.

Componentes considerados:

- Backend Flask desplegado en Amazon EC2.
- Archivos almacenados mediante Amazon S3.
- Base de datos PostgreSQL.
- Variables de entorno para configuración.

El sistema utilizará configuraciones externas para permitir cambiar entre ambientes sin modificar el código fuente.

---

# 5. Autenticación y autorización

El sistema implementará autenticación mediante tokens.

Flujo general:

1. El usuario ingresa sus credenciales.
2. El backend valida la información proporcionada.
3. Se genera un token de acceso.
4. El frontend almacena el token temporalmente.
5. Las solicitudes posteriores utilizan dicho token para acceder a recursos protegidos.

Funciones disponibles:

- Inicio de sesión.
- Cierre de sesión.
- Validación de sesión.
- Protección de rutas privadas.

El sistema manejará diferentes niveles de acceso mediante roles.

Roles principales:

- Administrador.
- Usuario estándar.

---

# 6. Operaciones CRUD

Los módulos administrativos implementarán operaciones CRUD:

- **Create:** creación de nuevos registros.
- **Read:** consulta de información existente.
- **Update:** modificación de información.
- **Delete:** eliminación de registros.

Estas operaciones estarán disponibles para:

- Usuarios.
- Convocatorias.
- Proyectos.
- Documentos registrados.

---

# 7. Módulos del sistema

## 7.1 Módulo de autenticación

Permite controlar el acceso al sistema.

Funciones:

- Inicio de sesión.
- Cierre de sesión.
- Manejo de tokens.
- Protección de rutas.

---

## 7.2 Administración de usuarios

Permite gestionar usuarios registrados.

Operaciones:

- Alta de usuarios.
- Consulta de usuarios.
- Modificación de información.
- Eliminación de usuarios.

Información administrada:

- Datos personales.
- Credenciales.
- Roles.
- Estado del usuario.

---

## 7.3 Gestión de convocatorias

Permite administrar convocatorias disponibles.

Funciones:

- Crear convocatorias.
- Consultar convocatorias.
- Modificar información.
- Eliminar convocatorias.

Información gestionada:

- Nombre.
- Descripción.
- Fechas.
- Estado.

---

## 7.4 Gestión de proyectos

Permite registrar y administrar proyectos asociados a convocatorias.

Funciones:

- Crear proyectos.
- Consultar proyectos.
- Modificar información.
- Eliminar proyectos.

Información almacenada:

- Datos generales.
- Usuario responsable.
- Convocatoria relacionada.
- Documentos asociados.

---

## 7.5 Gestión de documentos

Permite administrar archivos asociados al sistema.

Funciones:

- Carga de documentos.
- Consulta de documentos.
- Descarga de archivos.
- Asociación con proyectos o usuarios.

Los archivos serán almacenados en Amazon S3.

---

## 7.6 Dashboard estadístico

El sistema contará con un panel de información general.

Indicadores principales:

- Número de usuarios registrados.
- Cantidad de convocatorias.
- Número de proyectos.
- Cantidad de archivos registrados.

---

## 7.7 Historial de cargas

Permitirá consultar las acciones relacionadas con documentos.

Información registrada:

- Usuario responsable.
- Archivo cargado.
- Fecha y hora.
- Proyecto relacionado.
- Referencia del archivo almacenado.

---

## 7.8 Perfil de usuario

Permitirá modificar información personal.

Funciones:

- Actualización de datos personales.
- Cambio de contraseña.
- Actualización de fotografía de perfil.

La fotografía será almacenada utilizando Amazon S3.

---

# 8. Seguridad del sistema

El sistema considerará mecanismos de seguridad como:

- Autenticación mediante tokens.
- Protección de rutas privadas.
- Control basado en roles.
- Validación de archivos.
- Manejo seguro de credenciales.
- Uso de permisos mediante IAM.

Las credenciales sensibles deberán manejarse mediante variables de entorno y nunca almacenarse directamente dentro del código fuente.

---

# 9. Estructura general del proyecto

```
ProjectHub/
├── backend/                          # API REST en Flask
│   ├── documentation/                # Documentación técnica del backend
│   ├── extensions/                   # Extensiones de Flask (DB, JWT, CORS)
│   ├── migrations/                   # Migraciones de base de datos (Alembic)
│   ├── seed/                         # Scripts de seed en Python puro
│   ├── src/
│   │   ├── config/                   # Configuración por entorno
│   │   ├── middleware/               # Middleware personalizados
│   │   ├── models/                   # Modelos SQLAlchemy
│   │   ├── modules/                  # Módulos funcionales (auth, users, ...)
│   │   │   ├── auth/                 # Módulo de autenticación
│   │   │   └── users/                # Módulo de administración de usuarios
│   │   ├── services/                 # Servicios transversales (StorageService)
│   │   ├── static/
│   │   │   └── defaults/             # Assets por defecto del sistema
│   │   └── utils/                    # Utilidades generales
│   ├── factory.py                    # Application Factory
│   ├── run.py                        # Punto de entrada de desarrollo
│   ├── requirements.txt              # Dependencias Python
│   └── wsgi.py                       # Punto de entrada WSGI para producción
│
├── frontend/                         # Aplicación Vue.js
│   ├── documentation/                # Documentación técnica del frontend
│   ├── public/                       # Assets públicos estáticos
│   ├── src/
│   │   ├── api/                      # Configuración de cliente HTTP (Axios)
│   │   ├── layouts/                  # Layouts de la aplicación
│   │   ├── modules/                  # Módulos funcionales
│   │   │   ├── auth/                 # Login / Registro
│   │   │   ├── dashboard/            # Panel principal y estadísticas
│   │   │   └── user/                 # Gestión de usuarios
│   │   ├── router/                   # Configuración de Vue Router
│   │   ├── stores/                   # Pinia stores (auth, etc.)
│   │   ├── views/                    # Vistas generales
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json                  # Dependencias npm
│   └── vite.config.ts                # Configuración Vite
│
├── database/                         # Scripts y documentación de BD
├── documentation/                    # Documentación general del proyecto
│   ├── Alcance.md                    # Este documento
│   ├── Architecture.md
│   └── PROJECT_GUIDE.md
├── docker-compose.yml                # Orquestación para entorno local
└── README.md
```


---

# 10. Entregables del proyecto

La entrega final deberá realizarse dentro de un archivo comprimido `.zip`.

Debe contener:

## Código fuente completo

Incluyendo:

- Código del frontend.
- Código del backend.
- Archivos de configuración necesarios.

---

## Script de base de datos

Archivo:

# database.sql

Debe incluir:

- Creación de tablas.
- Relaciones.
- Restricciones.
- Datos iniciales necesarios.

---

## Documento PDF

Debe contener:

- Descripción general del proyecto.
- Arquitectura utilizada.
- Tecnologías implementadas.
- Servicios AWS empleados.
- Capturas del funcionamiento del sistema.

---

## Dirección de acceso

Debe incluir:

- Dirección IP pública de la instancia EC2.

o

- URL pública de la aplicación desplegada.

---

## Video de demostración

Duración aproximada:
- 5 a 10 minutos


Debe mostrar:

- Inicio de sesión.
- Operaciones CRUD.
- Gestión de usuarios.
- Gestión de convocatorias.
- Gestión de proyectos.
- Carga de documentos.
- Consulta y descarga de archivos almacenados en Amazon S3.
- Funcionamiento del sistema desplegado.

El video podrá ser compartido mediante:

- YouTube público.
- Google Drive mediante enlace compartido.

---

# 11. Validación antes de entrega

Es responsabilidad del estudiante verificar que:

- El archivo `.zip` contenga todos los elementos solicitados.
- El código fuente pueda ejecutarse correctamente.
- El script SQL funcione correctamente.
- Los enlaces proporcionados sean accesibles.
- Las evidencias solicitadas puedan visualizarse.
- El sistema desplegado se encuentre disponible.

---

# 12. Tecnologías principales

| Componente | Tecnología |
|------------|------------|
| Frontend | Vue.js |
| Framework visual | Bootstrap 5/ tailwindcss | 
| Backend | Flask |
| API | REST API |
| Lenguaje Backend | Python |
| Base de datos | PostgreSQL |
| Almacenamiento | Amazon S3 |
| Infraestructura | Amazon EC2 |
| Seguridad | AWS IAM |
| Autenticación | Tokens |