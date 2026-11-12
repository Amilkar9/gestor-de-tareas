# Task Flow

Aplicación web moderna desarrollada con arquitectura hexagonal, clean code y principios SOLID.

## Problema resuelto

La aplicación permite gestionar tareas diarias de trabajo o estudio, con estado de completitud, creación, consulta, actualización y eliminación.

## Stack

- Backend: Flask
- Frontend: React + Vite
- Base de datos: SQLite

## Arquitectura

La solución está organizada en capas:

- domain: entidades y puertos del repositorio
- application: casos de uso
- infrastructure: adaptadores de persistencia y rutas HTTP

## Estructura del proyecto

```text
backend/
  app/
    domain/
    application/
    infrastructure/
  tests/
  requirements.txt
  run.py
frontend/
  src/
  package.json
  vite.config.js
```

## Requisitos

- Python 3.11+
- Node.js 18+

## Instalación del backend

```bash
cd backend
python -m pip install -r requirements.txt
```

## Ejecutar backend

```bash
cd backend
python run.py
```

La API queda disponible en:

- http://localhost:5000/api/tasks

## Instalación del frontend

```bash
cd frontend
npm install
```

## Ejecutar frontend

```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

Abre la interfaz en:

- http://localhost:4173/

## Endpoints principales

- GET /api/tasks
- POST /api/tasks
- PATCH /api/tasks/<id>/toggle
- DELETE /api/tasks/<id>

## Principios aplicados

- Inversión de dependencias: el caso de uso depende de la interfaz del repositorio.
- Encapsulamiento: la lógica de validación vive en la capa de dominio.
- Separación de responsabilidades: persistencia, API y casos de uso no se mezclan.
- Código limpio: nombres claros, métodos pequeños, validación explícita.
