# API-003 Listar cuentas del usuario autenticado

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna las cuentas asociadas al usuario autenticado.

## Endpoint

- metodo: `GET`
- ruta: `/api/email-accounts/byuser`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{}
```

## Response esperada

### Exito

```json
[
  {}
]
```

## Errores esperados

- `401`: no autenticado

## Notas tecnicas

- delega a `app.services.email_account_service.get_email_accounts_by_user`
- siempre retorna una lista, incluso vacia
