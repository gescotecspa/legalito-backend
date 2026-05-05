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
  "lastName": "Lovelace",
  "terms_id": 2,
  "terms_version": "v2",
  "accepted_terms": true
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
- `400`: falta `terms_id`
- `400`: falta `terms_version`
- `400`: falta `accepted_terms`
- `400`: `accepted_terms` no fue confirmado en `true`
- `409`: email ya registrado
- `409`: no hay terminos vigentes disponibles
- `409`: `terms_id` no corresponde a la ultima version vigente
- `409`: `terms_version` no corresponde a la ultima version vigente
- `415`: request no JSON

## Notas tecnicas

- delega a `app.services.user_service.register_user`
- requiere que exista `Status(active)` y una version vigente de `terms_and_conditions`
- exige `terms_id` para validar que el frontend este registrando contra la version vigente mostrada al usuario
- exige `terms_version` para reforzar que el frontend este registrando la misma version visible al usuario
- exige `accepted_terms=true` para confirmar aceptacion explicita en el momento del registro
- tiene coverage automatizada de `415` y `409`
- fue validado manualmente en dev y QA
