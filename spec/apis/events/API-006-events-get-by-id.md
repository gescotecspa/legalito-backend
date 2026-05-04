# API-006 Obtener evento por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que obtiene un evento por su identificador.

## Endpoint

- metodo: `GET`
- ruta: `/api/events/<event_id>`

## Autenticacion

- protegida con JWT

## Request

### Path params

- `event_id`: identificador del evento a consultar

## Response esperada

### Exito

```json
{
  "id": 15,
  "user": "user@example.com",
  "title": "Audiencia preparatoria",
  "description": "Sala 2",
  "start_date": "2026-05-10T09:30:00",
  "type_id": 12
}
```

## Errores esperados

- `401`: no autenticado
- `404`: evento inexistente o sin ownership para el usuario autenticado

## Notas tecnicas

- usa `get_jwt_identity()` como fuente del usuario autenticado
- delega a `app.services.event_service.get_event_by_id_service`
- valida ownership consultando el evento por `id` y `user`
