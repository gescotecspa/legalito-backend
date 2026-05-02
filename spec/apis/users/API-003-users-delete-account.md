# API-003 Eliminar cuenta

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina logicamente una cuenta de usuario validando email y contraseña.

## Endpoint

- metodo: `POST`
- ruta: `/api/users/delete-account`

## Autenticacion

- publica

## Request

### Body

```json
{
  "email": "user@example.com",
  "password": "Secret123!"
}
```

## Response esperada

### Exito

```json
{
  "message": "Cuenta eliminada exitosamente"
}
```

## Errores esperados

- `400`: email o contraseña faltantes
- `401`: contraseña incorrecta
- `404`: usuario no encontrado

## Notas tecnicas

- delega a `app.services.user_service.delete_user`
- el flujo realiza eliminacion logica, no borrado fisico
- cambia el estado del usuario a `deleted`
- tiene coverage automatizada de `400`, `401` y `404`
