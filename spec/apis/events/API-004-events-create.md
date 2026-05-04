# API-004 Crear evento persistido

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que crea un evento persistido para el usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/events/create`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "title": "Audiencia preparatoria",
  "start_date": "2026-05-10T09:30:00",
  "description": "Sala 2",
  "type_id": 12
}
```

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

- `400`: faltan `title` o `start_date`
- `400`: formato de fecha invalido
- `400`: usuario autenticado inexistente
- `400`: tipo de evento inexistente
- `401`: no autenticado

## Notas tecnicas

- usa `get_jwt_identity()` para definir el owner del evento
- delega a `app.services.event_service.create_event`
- valida `type_id` solo si viene informado
- persiste el evento antes de responder
