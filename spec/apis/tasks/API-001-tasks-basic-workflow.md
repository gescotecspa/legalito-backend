# API-001 Tasks Basic Workflow

## Estado

Implementado

## Objetivo

Describir los endpoints basicos de tareas para el primer corte CRM legal.

## Autenticacion

Requiere `Bearer token` en todos los endpoints.

## Endpoints

### `GET /api/tasks`

Lista tareas propias. Acepta filtros opcionales.

Query params:

- `case_id`: filtra por causa
- `client_id`: filtra por cliente
- `include_completed`: `true` o `false`

### `POST /api/tasks`

Crea una tarea asociada al JWT.

Request:

```json
{
  "title": "Preparar escrito",
  "description": "Revisar antecedentes",
  "priority": "normal",
  "due_date": "2026-08-01",
  "assignee_user": "user@example.com",
  "case_id": 1,
  "client_id": 1
}
```

### `GET /api/tasks/<task_id>`

Obtiene una tarea propia.

### `PUT /api/tasks/<task_id>`

Actualiza una tarea propia.

### `POST /api/tasks/<task_id>/complete`

Marca una tarea propia como completada.

## Response esperada

```json
{
  "id": 1,
  "owner_user": "user@example.com",
  "title": "Preparar escrito",
  "description": "Revisar antecedentes",
  "status": "pending",
  "priority": "normal",
  "due_date": "2026-08-01T00:00:00",
  "assignee_user": "user@example.com",
  "case_id": 1,
  "client_id": 1,
  "completed_at": null,
  "created_at": "2026-07-24T23:10:00",
  "updated_at": "2026-07-24T23:10:00"
}
```

## Errores esperados

- `400`: datos invalidos, falta `title`, estado/prioridad invalida o vinculo no visible
- `401`: falta autenticacion
- `404`: tarea inexistente o fuera del ownership
- `500`: error inesperado

## Notas tecnicas

- `owner_user` se obtiene desde JWT.
- `case_id` se valida contra `cases_users`.
- `client_id` se valida contra `clients.owner_user`.
- completar una tarea asigna `status = completed` y `completed_at`.

## Estado de pruebas

- Unit tests: implementado
- Integration tests: parcial
- E2E: pendiente

Cobertura actual:

- `GET /tasks` requiere JWT y usa identidad autenticada
- `POST /tasks` usa identidad autenticada
- `GET /tasks/<id>` rechaza tarea fuera de ownership
- `POST /tasks/<id>/complete` usa identidad autenticada
- servicios cubren validaciones, ownership, creacion, actualizacion y completado

