# ProjectHub

Este es el repositorio principal para ProjectHub, una aplicación full-stack construida con Vue 3 (frontend) y Flask (backend).

## Estructura del Proyecto

```
# El árbol completo del proyecto se generará aquí.
```

## Backend (Python/Flask)

### Requisitos

- Python 3.12+
- pip
- PostgreSQL

### Configuración del Entorno Virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
pip install -r backend/requirements.txt
```

### Ejecución

```bash
# En desarrollo
cd backend
flask run
```

## Frontend (Vue 3)

### Requisitos

- Node.js (LTS)
- npm o yarn

### Instalación de Dependencias

```bash
cd frontend
npm install  # o yarn install
```

### Ejecución

```bash
cd frontend
npm run dev  # o yarn dev
```

## Base de Datos (PostgreSQL)

Se recomienda usar Docker Compose para configurar la base de datos localmente.

### Configuración con Docker Compose

```bash
docker-compose up -d postgres
```

## Contribución

Este proyecto está en desarrollo. Las contribuciones son bienvenidas siguiendo las guías de estilo y arquitectura.
