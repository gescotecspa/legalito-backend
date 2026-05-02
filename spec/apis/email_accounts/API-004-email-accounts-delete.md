# API-004 Eliminar cuenta de correo

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina una cuenta del usuario autenticado.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/email-accounts`

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
  "message": "Account successfully deleted"
}
```

## Errores esperados

- `401`: no autenticado
- `404`: cuenta inexistente o no eliminable
- `500`: error inesperado al eliminar

## Notas tecnicas

- delega a `app.services.email_account_service.delete_email_accounts`
- el servicio resuelve la cuenta por `email_address` y `user`
