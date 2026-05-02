# API-004 Listar notificaciones por usuario autenticado

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna notificaciones activas del usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/notifications/byUser`

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

- delega a `app.services.notification_service.get_notifications_by_user`
- ignora cualquier `user` forjado en body y usa la identidad JWT
- el servicio filtra por `status = "active"` y ordena por `received_date`
