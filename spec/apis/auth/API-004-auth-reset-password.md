# API-004 Confirmar recuperacion de contraseña

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que confirma un cambio de contraseña usando codigo temporal.

## Endpoint

- metodo: `POST`
- ruta: `/api/auth/reset-password`

## Autenticacion

- publica

## Request

### Body

```json
{
  "email": "user@example.com",
  "reset_code": "123456",
  "password": "NewSecret123!"
}
```

## Response esperada

### Exito

```json
{
  "message": "Password successfully updated"
}
```

## Errores esperados

- `400`: campos faltantes
- `400`: codigo invalido o expirado
- `404`: usuario no encontrado
- `429`: rate limiting excedido

## Notas tecnicas

- delega a `app.services.auth_service.reset_password_with_code`
- el flujo vigente usa codigo temporal de 6 digitos
- tiene coverage automatizada de validacion, codigo invalido, codigo expirado y `429`
