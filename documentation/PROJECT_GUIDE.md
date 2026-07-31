# PROJECT_GUIDE.md

## Propósito
Este documento sirve como la guía maestra y punto de entrada principal para el proyecto ProjectHub. Su propósito es proporcionar una visión general de alto nivel del proyecto, sus objetivos, principios rectores y la estructura general de la documentación, asegurando que todos los colaboradores tengan una comprensión unificada.

## Alcance
Este documento abarca la visión general del proyecto, los objetivos, el stack tecnológico y la organización de la documentación. No profundiza en detalles técnicos específicos de implementación, los cuales se encuentran en documentos dedicados.

## Índice
- [Visión General del Proyecto](#visión-general-del-proyecto)
- [Objetivos del Proyecto](#objetivos-del-proyecto)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura de la Documentación](#estructura-de-la-documentación)
- [Principios Rectores](#principios-rectores)
- [Glosario](#glosario)
- [Notas Importantes](#notas-importantes)

## Visión General del Proyecto
ProjectHub es una aplicación web diseñada para la gestión integral de diversos aspectos relacionados con proyectos, incluyendo:
- **Usuarios**: Gestión de perfiles y roles.
- **Autenticación**: Mecanismos de seguridad para acceso al sistema.
- **Convocatorias**: Administración de procesos de postulación o participación.
- **Proyectos**: Creación, seguimiento y gestión de proyectos.
- **Documentos**: Almacenamiento y organización de archivos relacionados.
- **Dashboard**: Panel de control con información relevante y métricas.
- **Perfil de Usuario**: Configuración y visualización de la información del usuario.

## Objetivos del Proyecto
- Proveer una plataforma robusta y escalable para la gestión de proyectos.
- Facilitar la colaboración entre usuarios.
- Reforzar conocimientos fundamentales de desarrollo Full Stack, Flask, Vue, PostgreSQL y AWS para el desarrollador principal.
- Mantener una documentación exhaustiva y actualizada a lo largo del ciclo de vida del proyecto.

## Stack Tecnológico

### Frontend
- **Framework**: Vue 3 (Composition API)
- **Manejo de Rutas**: Vue Router
- **Gestión de Estado**: Pinia
- **Peticiones HTTP**: Axios
- **UI Framework**: Bootstrap 5

### Backend
- **Lenguaje**: Python 3.12
- **Framework**: Flask
- **Modularización**: Flask Blueprints
- **ORM**: SQLAlchemy
- **Migraciones de Base de Datos**: Flask-Migrate
- **Autenticación JWT**: Flask-JWT-Extended
- **Manejo de CORS**: Flask-CORS
- **Integración AWS**: boto3
- **Driver PostgreSQL**: psycopg2
- **Variables de Entorno**: python-dotenv

### Base de Datos
- **Sistema**: PostgreSQL

### Cloud
- **Servidor**: Amazon EC2
- **Almacenamiento**: Amazon S3
- **Gestión de Acceso**: AWS IAM

### Sistema Operativo de Desarrollo
- Windows

## Estructura de la Documentación
La documentación del proyecto se organiza de la siguiente manera:
- **`/documentation`**: Documentación general del proyecto.
  - `AI_GUIDELINES.md`: Directrices para la colaboración con IA.
  - `PROJECT_GUIDE.md`: Guía maestra del proyecto (este documento).
  - `Architecture.md`: Documentación de la arquitectura general.
  - `Database.md`: Documentación del modelo de datos.
  - `AWS.md`: Documentación de la infraestructura y servicios AWS.
  - `API.md`: Documentación de los endpoints de la API.
  - `Deployment.md`: Proceso de despliegue.
  - `Changelog.md`: Registro de cambios del proyecto.
  - `Roadmap.md`: Plan de desarrollo y evolución del proyecto.
- **`/backend/documentation`**: Documentación específica del backend.
  - `README.md`: Introducción al backend.
  - `Architecture.md`: Arquitectura del backend.
  - `Modules.md`: Descripción de módulos y funcionalidades.
  - `Authentication.md`: Detalles de la autenticación.
  - `Database.md`: Integración con la base de datos (backend).
  - `API.md`: Documentación detallada de la API del backend.
- **`/frontend/documentation`**: Documentación específica del frontend.
  - `README.md`: Introducción al frontend.
  - `Architecture.md`: Arquitectura del frontend.
  - `Views.md`: Descripción de vistas y pantallas.
  - `Components.md`: Componentes reutilizables.
  - `Stores.md`: Gestión de estado con Pinia.
  - `Routing.md`: Estrategias de enrutamiento.

## Principios Rectores
- **Claridad**: La documentación debe ser fácil de entender para cualquier lector, independientemente de su nivel técnico.
- **Consistencia**: Mantener un estilo y formato uniforme en toda la documentación.
- **Actualización Continua**: La documentación debe reflejar siempre el estado actual del proyecto.
- **Profesionalismo**: Redacción técnica precisa y bien estructurada.

## Glosario
- **AI**: Inteligencia Artificial.
- **API**: Application Programming Interface.
- **AWS**: Amazon Web Services.
- **CORS**: Cross-Origin Resource Sharing.
- **JWT**: JSON Web Token.
- **ORM**: Object-Relational Mapping.

## Notas Importantes
- Este documento es un punto de partida y evolucionará con el proyecto.
- Se recomienda revisar periódicamente este documento para mantenerse al tanto de los cambios y la evolución del proyecto.

## Convenciones
- Los comandos de Python deberán utilizar siempre `py`.

## Pendiente de implementación
- Diagrama de la estructura de la documentación (Mermaid).