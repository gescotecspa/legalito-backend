# API-005 Alternar estado de cuenta de correo

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que activa o desactiva una cuenta del usuario autenticado.

## Endpoint

- metodo: `PUT`
- ruta: `/api/email-accounts/toggle-status`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "email": "buzon@example.com"
}
```

## Response esperada

### Exito

```json
{
  "message": "Account status changed successfully. Now active",
  "active": true
}
```

## Errores esperados

- `401`: no autenticado
- `404`: cuenta inexistente o no actualizable
- `500`: error inesperado al alternar estado

## Notas tecnicas

- delega a `app.services.email_account_service.toggle_email_account_status`
- el servicio alterna el booleano `active`
