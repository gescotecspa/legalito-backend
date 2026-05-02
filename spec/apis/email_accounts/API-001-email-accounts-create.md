# API-001 Crear cuenta de correo

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que registra una cuenta de correo para el usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/email-accounts`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "provider": "gmail",
  "imap_server": "imap.gmail.com",
  "email_address": "buzon@example.com",
  "password": "app-password"
}
```

## Response esperada

### Exito

```json
{
  "message": "Account successfully added",
  "account": {}
}
```

## Errores esperados

- `400`: usuario inexistente o cuenta duplicada
- `401`: no autenticado
- `500`: error inesperado de persistencia

## Notas tecnicas

- delega a `app.services.email_account_service.add_email_account`
- inyecta `user` desde JWT antes de llamar al servicio
- la serializacion ya no expone `password`
