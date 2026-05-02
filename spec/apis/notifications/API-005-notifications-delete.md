# API-005 Eliminar notificacion

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina una notificacion del usuario autenticado.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/notifications/<notification_id>`

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
{
  "message": "Notification deleted successfully."
}
```

## Errores esperados

- `401`: no autenticado
- `404`: notificacion inexistente o fuera del ownership del usuario autenticado
- `500`: error inesperado al eliminar

## Notas tecnicas

- delega a `app.services.notification_service.delete_notification`
- usa el `user` del JWT para restringir el delete
