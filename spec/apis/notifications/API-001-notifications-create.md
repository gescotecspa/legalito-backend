# API-001 Crear notificacion

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que crea una notificacion.

## Endpoint

- metodo: `POST`
- ruta: `/api/notifications`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "subject": "Citacion a audiencia",
  "sender": "tribunal@example.com",
  "received_date": "2026-05-01T10:00:00",
  "body": "Detalle del mensaje",
  "status": "pending",
  "user": "owner@example.com"
}
```

## Response esperada

### Exito

```json
{
  "message": "Notification created successfully.",
  "notification": {}
}
```

## Errores esperados

- `400`: faltan `subject`, `sender` o `received_date`
- `401`: no autenticado
- `500`: error inesperado de persistencia

## Notas tecnicas

- delega a `app.services.notification_service.create_notification`
- convierte `received_date` desde ISO string a `datetime`
- hoy acepta `user` en body y no lo sobreescribe con JWT; conviene revisarlo si el endpoint pasa a uso interactivo directo
