# Configuración CORS del Backend

El backend de ProjectHub utiliza la extensión `Flask-CORS` para gestionar la política de "Cross-Origin Resource Sharing" (CORS). Esto es crucial para permitir que aplicaciones frontend (como la aplicación Vue.js) interactúen con la API del backend cuando se ejecutan en diferentes dominios o puertos.

## Configuración

Las políticas de CORS se configuran a través de la variable de entorno `CORS_ORIGINS`.

### `CORS_ORIGINS`

Esta variable de entorno define los orígenes (dominios) permitidos para acceder a los recursos del backend.

*   **Valores aceptados:**
    *   Una lista de URLs separadas por comas (`,`). Por ejemplo: `"http://localhost:8080,https://myfrontend.com"`
    *   `"*"`: Para permitir el acceso desde cualquier origen (uso recomendado solo para desarrollo o APIs públicas).

*   **Ejemplo de uso en `.env`:**

    Para desarrollo local:
    ```
    CORS_ORIGINS=http://localhost:8080
    ```

    Para múltiples orígenes en producción:
    ```
    CORS_ORIGINS=https://mi-dominio-frontend.com,https://otro-dominio.com
    ```

    Para permitir todos los orígenes (menos seguro, solo para desarrollo o si se entiende el riesgo):
    ```
    CORS_ORIGINS=*
    ```

### Implementación en `factory.py`

El archivo `backend/factory.py` lee esta variable de entorno al inicializar la aplicación Flask:

```python
import os
from dotenv import load_dotenv
from extensions.cors import cors

# ... (otras inicializaciones)

# Cargar variables de entorno
load_dotenv()

# ...

def create_app():
    app = Flask(__name__)
    # ...

    cors_origins_env = os.getenv("CORS_ORIGINS")
    if cors_origins_env:
        allowed_origins = [origin.strip() for origin in cors_origins_env.split(',')]
    else:
        allowed_origins = ["*"] # Por defecto, permite todos los orígenes si no se especifica

    cors.init_app(
        app,
        resources={r"/api/.*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Headers"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    # ...
    return app
```

Asegúrese de configurar `CORS_ORIGINS` adecuadamente en su archivo `.env` o en la configuración de su entorno de despliegue.
