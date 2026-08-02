# Refactorización de la Arquitectura del Backend: Repository -> Service -> Controller -> Routes (Modular)

Este documento detalla la refactorización implementada en el backend de Flask para adoptar un patrón de diseño **modular** y robusto, siguiendo la estructura de **Repository, Service, Controller, Routes** por cada módulo funcional.

## Racional y Beneficios

La arquitectura original mezclaba responsabilidades, lo que dificultaba la escalabilidad, el mantenimiento y las pruebas. Al introducir esta nueva separación de capas **dentro de cada módulo**, logramos los siguientes beneficios adicionales:

*   **Modularidad Mejorada**: Cada módulo es una unidad autónoma con sus propias capas, lo que facilita el desarrollo, las pruebas y el despliegue de funcionalidades específicas.
*   **Aislamiento de Cambios**: Los cambios en un módulo tienen un impacto mínimo en otros módulos, reduciendo el riesgo de efectos secundarios no deseados.
*   **Claridad Estructural**: La organización por módulos hace que la estructura del proyecto sea más intuitiva y fácil de navegar.
*   **Separación de Responsabilidades (SOC)**: Cada capa tiene una única razón para cambiar, lo que hace el código más fácil de entender y modificar.
*   **Mayor Mantenibilidad**: Los cambios en la lógica de negocio no afectan directamente la capa de persistencia ni la de presentación, y viceversa.
*   **Facilidad de Pruebas**: Cada capa puede ser probada de forma independiente (ej. mockear el repositorio para probar el servicio, mockear el servicio para probar el controlador).
*   **Reusabilidad**: La lógica de negocio y de acceso a datos es más fácil de reutilizar en diferentes contextos (ej. una CLI, otro tipo de API).
*   **Flexibilidad Tecnológica**: Permite cambiar la tecnología de la base de datos o el framework web con menor impacto en otras partes del sistema.

## Descripción de las Capas

### 1. Repository (Capa de Persistencia)

*   **Propósito**: Encapsula la lógica necesaria para acceder a los datos de una entidad específica dentro de un módulo.
*   **Responsabilidades**:
    *   Manejar todas las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para una entidad específica (ej. `User`).
    *   Interactuar directamente con el ORM (SQLAlchemy en este caso).
    *   Convertir los resultados del ORM en objetos de dominio (o modelos en este caso).
*   **Ubicación**: El archivo de repositorio reside en la raíz del directorio del módulo correspondiente. Por ejemplo, `backend/src/modules/users/user_repository.py`.
*   **Cambios Realizados**: Toda la lógica `User.query.*`, `db.session.add()`, `db.session.commit()`, `db.session.delete()` se ha movido a `user_repository.py` dentro del módulo `users`.

### 2. Service (Capa de Lógica de Negocio)

*   **Propósito**: Contiene la lógica de negocio central de un módulo.
*   **Responsabilidades**:
    *   Coordinar las operaciones de uno o más repositorios (incluso de otros módulos si es necesario).
    *   Implementar validaciones de negocio.
    *   Realizar transformaciones de datos o cálculos específicos del dominio.
*   **Ubicación**: El archivo de servicio reside en la raíz del directorio del módulo correspondiente. Por ejemplo, `backend/src/modules/users/user_service.py`, `backend/src/modules/auth/auth_service.py`.
*   **Cambios Realizados**: Los servicios (`UserService`, `AuthService`) ahora dependen de los repositorios de sus respectivos módulos (o de otros módulos, como `AuthService` usando `UserRepository`) para todas las interacciones con la base de datos. Se han eliminado las llamadas directas a `User.query` y `db.session`, reemplazándolas por llamadas a los métodos del repositorio.

### 3. Controller (Capa de Control de Solicitudes)

*   **Propósito**: Manejar las solicitudes HTTP entrantes para un módulo y coordinar la respuesta.
*   **Responsabilidades**:
    *   Parsear los datos de la solicitud (ej. `request.get_json()`).
    *   Delegar la lógica de negocio al servicio correspondiente del módulo.
    *   Construir la respuesta HTTP (ej. `jsonify`) con el código de estado adecuado.
    *   Manejar excepciones específicas de la API y devolver mensajes de error apropiados.
*   **Ubicación**: El archivo de controlador reside en la raíz del directorio del módulo correspondiente. Por ejemplo, `backend/src/modules/users/user_controller.py`, `backend/src/modules/auth/auth_controller.py`.
*   **Cambios Realizados**: Las funciones que antes manejaban directamente las solicitudes en los `routes.py` de cada módulo han sido movidas a métodos estáticos dentro de las clases de controlador (`UserController`, `AuthController`). Incluyen el manejo de `request`, `jsonify` y la captura de errores específicos para devolver una respuesta HTTP.

### 4. Routes (Capa de Enrutamiento)

*   **Propósito**: Mapear URLs a los métodos de los controladores de un módulo.
*   **Responsabilidades**:
    *   Definir los endpoints de la API para el módulo (usando `Blueprint` y `@route`).
    *   Delegar inmediatamente la ejecución al método apropiado del controlador del módulo.
*   **Ubicación**: El archivo de rutas reside en la raíz del directorio del módulo correspondiente. Por ejemplo, `backend/src/modules/users/routes.py`, `backend/src/modules/auth/routes.py`.
*   **Cambios Realizados**: Estos archivos ahora son muy "delgados", importando solo el `Blueprint` y el `Controller` correspondiente de su módulo, y mapeando cada ruta a un método del controlador. Se han eliminado toda la lógica de `request`, `jsonify`, `UserService`, `AuthService`, `UserRepository` de estos archivos.

## Impacto en el Código Base

*   **Carpeta `backend/src`**: Se ha creado una carpeta `src` en el directorio `backend/` y el directorio `modules` junto con otros directorios principales (`config`, `extensions`, `middleware`, `migrations`, `models`, `services`, `tests`, `utils`) se han movido dentro de ella (`backend/src/...`).
*   **Estructura de Módulos Aplanada**: Las subcarpetas `repositories` y `controllers` dentro de cada módulo (`users`, `auth`) han sido eliminadas. Los archivos de repositorio y controlador ahora residen directamente en la raíz de su respectivo módulo.
*   **Archivos de Repositorio**:
    *   `backend/src/modules/users/user_repository.py`: Contiene los métodos para interactuar con el modelo `User` en la base de datos.
    *   `backend/src/modules/auth/auth_repository.py`: Se creó este repositorio minimalista para mantener la consistencia de la arquitectura, aunque `AuthService` utiliza `UserRepository` del módulo `users` para operaciones de `User`. (Los directorios `backend/src/modules/auth/repositories` y `backend/src/modules/users/repositories` no pudieron ser eliminados debido a errores de permisos, pero están vacíos y no afectan la funcionalidad).
*   **Archivos de Controlador**:
    *   `backend/src/modules/users/user_controller.py`: Contiene los métodos que manejan las solicitudes HTTP para los recursos de usuario.
    *   `backend/src/modules/auth/auth_controller.py`: Contiene los métodos que manejan las solicitudes HTTP para la autenticación.
*   **Archivos `*_service.py`**:
    *   `backend/src/modules/users/user_service.py`: Modificado para usar `user_repository.py` del módulo `users`.
    *   `backend/src/modules/auth/auth_service.py`: Modificado para usar `user_repository.py` del módulo `users`.
*   **Archivos `routes.py`**:
    *   `backend/src/modules/users/routes.py`: Modificado para usar `user_controller.py` del módulo `users`. (Los directorios `backend/src/modules/users/controllers` no pudieron ser eliminados debido a errores de permisos, pero están vacíos y no afectan la funcionalidad).
    *   `backend/src/modules/auth/routes.py`: Modificado para usar `auth_controller.py` del módulo `auth`. (Los directorios `backend/src/modules/auth/controllers` no pudieron ser eliminados debido a errores de permisos, pero están vacíos y no afectan la funcionalidad).
*   **Actualización de Imports**: Todos los imports en los archivos afectados, incluido `backend/factory.py`, han sido actualizados para reflejar la nueva estructura de directorios (`from src.models...`, `from src.extensions...`, `from src.modules...`).

Esta refactorización establece una base sólida para el crecimiento futuro del backend, facilitando la adición de nuevas funcionalidades y la comprensión del flujo de la aplicación de una manera altamente modular y organizada.
