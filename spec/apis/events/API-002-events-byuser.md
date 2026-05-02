# API-002 Listar eventos por usuario autenticado

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista eventos del usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/events/byuser`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{}
```

## Response esperada

### Exito

```json
[]
```

## Errores esperados

- `400`: falta identidad de usuario
- `401`: no autenticado

## Notas tecnicas

- usa `get_jwt_identity()` como fuente principal del usuario
- ignora cualquier `user` forjado en request si hay JWT
- delega a `app.services.event_service.list_events_by_user_service`
- tiene cobertura automatizada de uso de identidad autenticada
