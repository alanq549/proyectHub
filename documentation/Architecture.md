# Architecture.md

## Propósito
Este documento describe la arquitectura general de ProjectHub, proporcionando una vista de alto nivel de los componentes principales, sus interacciones y las decisiones de diseño fundamentales que sustentan el sistema. Sirve como una referencia clave para entender cómo las diferentes partes del proyecto se conectan y funcionan en conjunto.

## Alcance
Este documento cubre la arquitectura a nivel de sistema, incluyendo la división entre frontend, backend y base de datos, así como la integración con servicios cloud. No detalla la arquitectura interna de cada componente (ej. microservicios específicos), que se documentarán en sus respectivas secciones.

## Índice
- [Visión General de la Arquitectura](#visión-general-de-la-arquitectura)
- [Diagrama de Arquitectura General](#diagrama-de-arquitectura-general)
- [Componentes Principales](#componentes-principales)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Base de Datos](#base-de-datos)
  - [Servicios Cloud](#servicios-cloud)
- [Flujo de Datos y Comunicación](#flujo-de-datos-y-comunicación)
- [Consideraciones de Diseño](#consideraciones-de-diseño)
- [Notas Importantes](#notas-importantes)

## Visión General de la Arquitectura
ProjectHub sigue un patrón de arquitectura cliente-servidor tradicional, con un frontend SPA (Single Page Application) que se comunica con un backend API RESTful. La persistencia de datos se gestiona mediante una base de datos relacional y se integra con servicios de AWS para diversas funcionalidades como almacenamiento y gestión de identidades.

## Diagrama de Arquitectura General

```mermaid
graph LR
    User[Usuario] --> Frontend[Frontend Vue.js]
    Frontend --> |API REST| Backend[Backend Flask]
    Backend --> |SQLAlchemy / psycopg2| Database[PostgreSQL Database]
    Backend --> |boto3| AWS[Servicios AWS]
    AWS --> S3[Amazon S3]
    AWS --> IAM[AWS IAM]
    Database --> EC2[Amazon EC2 (hosting)]
```

**Descripción del Diagrama:**
- **Usuario**: Interactúa directamente con la aplicación web.
- **Frontend Vue.js**: La interfaz de usuario construida con Vue 3, Composition API, Vue Router, Pinia y Bootstrap 5. Se comunica con el Backend a través de una API REST.
- **Backend Flask**: El servidor de aplicaciones construido con Python 3.12, Flask, Flask Blueprints, SQLAlchemy, Flask-JWT-Extended y Flask-CORS. Es el cerebro de la aplicación, gestionando la lógica de negocio, la autenticación y la interacción con la base de datos y los servicios AWS.
- **PostgreSQL Database**: La base de datos relacional utilizada para la persistencia de datos, gestionada por SQLAlchemy y Flask-Migrate.
- **Servicios AWS**: Un conjunto de servicios de Amazon Web Services que proporcionan funcionalidades adicionales.
  - **Amazon S3**: Utilizado para almacenamiento de archivos (ej. documentos de proyectos).
  - **AWS IAM**: Gestión de identidades y accesos para asegurar la interacción con los servicios AWS.
  - **Amazon EC2**: La instancia donde se alojará y ejecutará la aplicación (Backend y Base de Datos).

## Componentes Principales

### Frontend
- Desarrollado con Vue 3 para una interfaz de usuario dinámica y reactiva.
- Utiliza Pinia para la gestión de estado global y Vue Router para el enrutamiento de SPA.
- Axios para realizar peticiones HTTP al backend.
- Bootstrap 5 proporciona un sistema de diseño responsivo y componentes UI.

### Backend
- Construido con Flask para una API RESTful ligera y modular.
- Los Flask Blueprints organizan la aplicación en módulos funcionales.
- SQLAlchemy como ORM para interactuar con la base de datos PostgreSQL.
- Flask-JWT-Extended para la autenticación basada en tokens JWT.
- Flask-CORS maneja las políticas de Cross-Origin Resource Sharing.
- `boto3` permite la interacción con los servicios de AWS.

### Base de Datos
- PostgreSQL como sistema de gestión de bases de datos relacionales (RDBMS).
- Flask-Migrate para gestionar las migraciones del esquema de la base de datos.

### Servicios Cloud
- **Amazon EC2**: Instancia de computación en la nube para el despliegue del backend y la base de datos.
- **Amazon S3**: Almacenamiento de objetos escalable para documentos y otros activos estáticos.
- **AWS IAM**: Gestión segura de acceso a recursos de AWS.

## Flujo de Datos y Comunicación
1. El usuario interactúa con el Frontend (Vue.js).
2. El Frontend realiza peticiones a la API REST del Backend (Flask) usando Axios.
3. El Backend procesa la lógica de negocio, interactúa con la Base de Datos (PostgreSQL) vía SQLAlchemy y/o con Servicios AWS (S3, IAM) vía boto3.
4. El Backend devuelve una respuesta al Frontend.
5. El Frontend actualiza la interfaz de usuario basándose en la respuesta del Backend.

## Consideraciones de Diseño
- **Escalabilidad**: La arquitectura está diseñada para permitir el escalado horizontal de los componentes de frontend y backend.
- **Seguridad**: Autenticación JWT, gestión de roles (futuro), y uso de AWS IAM para acceso seguro.
- **Modularidad**: Uso de Flask Blueprints en el backend y componentes/stores en el frontend para una organización clara y mantenimiento fácil.
- **Desacoplamiento**: Clara separación de responsabilidades entre frontend, backend y base de datos.

## Notas Importantes
- Este documento representa la arquitectura inicial y será actualizado conforme el proyecto evolucione y se tomen nuevas decisiones arquitectónicas.
- Se recomienda encarecidamente la implementación de un sistema de logging y monitoreo robusto.

## Pendiente de implementación
- Diagrama de componentes de Backend (Mermaid).
- Diagrama de componentes de Frontend (Mermaid).
- Estrategias de manejo de errores globales.
- Estrategias de caching.
- Definición de límites y cuotas para servicios AWS.
