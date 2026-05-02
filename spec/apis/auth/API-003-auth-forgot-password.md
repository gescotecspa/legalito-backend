# API-003 Solicitar recuperacion de contraseña

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que inicia la recuperacion de contraseña.

## Endpoint

- metodo: `POST`
- ruta: `/api/auth/forgot-password`

## Autenticacion

- publica

## Request

### Body

```json
{
  "email": "user@example.com"
}
```

## Response esperada

### Exito

```json
{
  "message": "A recovery code has been sent to your email"
}
```

## Errores esperados

- `400`: email faltante
- `404`: usuario no encontrado
- `429`: rate limiting excedido
- `502`: fallo del proveedor de correo

## Notas tecnicas

- delega a `app.services.auth_service.request_password_reset`
- no debe responder falso exito cuando falla el proveedor de envio
- tiene coverage automatizada de `404`, `429` y `502`
- en QA fue validado el comportamiento de error real con `502`
- Mailjet ya no esta disponible en QA y debe reemplazarse como proveedor
