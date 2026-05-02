# API-003 Editar evento propio

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que permite editar un evento perteneciente al usuario autenticado.

## Endpoint

- metodo: `PUT`
- ruta: `/api/events/edit/<event_id>`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "title": "Nuevo titulo",
  "start_date": "2026-05-01T10:00:00",
  "description": "Detalle",
  "type_id": 12
}
```

## Response esperada

### Exito

```json
{}
```

## Errores esperados

- `400`: formato de fecha invalido o tipo de evento inexistente
- `401`: no autenticado
- `404`: evento no encontrado o sin ownership

## Notas tecnicas

- valida ownership en `app.services.event_service.edit_event_service`
- usa `EventOwnershipException` para acceso a recursos ajenos
- tiene cobertura automatizada de ownership invalido
