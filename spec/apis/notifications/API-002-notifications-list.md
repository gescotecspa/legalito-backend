# API-002 Listar notificaciones

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna todas las notificaciones.

## Endpoint

- metodo: `GET`
- ruta: `/api/notifications/list`

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
[
  {}
]
```

## Errores esperados

- `401`: no autenticado
- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.notification_service.list_notifications`
- retorna el listado global sin filtrar por usuario
