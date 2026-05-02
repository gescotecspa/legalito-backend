# API-002 Registro de usuario

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint de registro de usuario.

## Endpoint

- metodo: `POST`
- ruta: `/api/auth/register`

## Autenticacion

- publica

## Request

### Body

```json
{
  "email": "user@example.com",
  "password": "Secret123!",
  "firstName": "Ada",
  "lastName": "Lovelace"
}
```

## Response esperada

### Exito

```json
{
  "message": "User successfully registered",
  "user": {
    "user": "user@example.com",
    "email": "user@example.com",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "status_id": 1,
    "terms_and_conditions_id": 1,
    "terms_version": "v1"
  }
}
```

## Errores esperados

- `400`: email o password faltantes
- `409`: email ya registrado
- `415`: request no JSON

## Notas tecnicas

- delega a `app.services.user_service.register_user`
- requiere que exista `Status(active)` y una version vigente de `terms_and_conditions`
- tiene coverage automatizada de `415` y `409`
- fue validado manualmente en dev y QA
