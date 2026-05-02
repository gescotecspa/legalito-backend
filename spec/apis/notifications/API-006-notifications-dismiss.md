# API-006 Descartar notificacion

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que marca una notificacion como descartada.

## Endpoint

- metodo: `POST`
- ruta: `/api/notifications/dismiss`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "id": 12
}
```

## Response esperada

### Exito

```json
true
```

## Errores esperados

- `401`: no autenticado
- `404`: notificacion inexistente o fuera del ownership del usuario autenticado
- `500`: error inesperado al descartar

## Notas tecnicas

- delega a `app.services.notification_service.dismiss`
- ignora cualquier `user` en body y usa la identidad JWT
- el servicio cambia `status` a `dismissed`
