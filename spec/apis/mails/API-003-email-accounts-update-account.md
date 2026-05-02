# API-003 Actualizar cuenta de correo propia

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que actualiza una cuenta de correo perteneciente al usuario autenticado.

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
  "email_address": "account@example.com",
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

- `400`: `email_address` ya en uso
- `401`: no autenticado
- `404`: cuenta no encontrada o sin ownership

## Notas tecnicas

- valida ownership en `app.services.email_account_service.update_email_account`
- mapea colision de correo a `400`
- mantiene oculto el `password` en la respuesta serializada
- tiene cobertura automatizada para ownership y colision de correo
