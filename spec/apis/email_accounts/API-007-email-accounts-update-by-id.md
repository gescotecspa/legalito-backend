# API-007 Actualizar cuenta de correo por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que actualiza una cuenta puntual respetando ownership.

## Endpoint

- metodo: `PUT`
- ruta: `/api/email-accounts/<id>`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "provider": "gmail",
  "imap_server": "imap.gmail.com",
  "email_address": "nuevo@example.com",
  "password": "app-password"
}
```

## Response esperada

### Exito

```json
{
  "message": "Account successfully updated",
  "account": {}
}
```

## Errores esperados

- `400`: email duplicado u otro error de validacion
- `401`: no autenticado
- `404`: cuenta inexistente o fuera del ownership del usuario autenticado
- `500`: error inesperado al actualizar

## Notas tecnicas

- delega a `app.services.email_account_service.update_email_account`
- tiene coverage automatizada basica para ownership y colision de `email_address`
