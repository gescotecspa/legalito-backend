# API-002 Listar todas las cuentas de correo

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna todas las cuentas registradas.

## Endpoint

- metodo: `GET`
- ruta: `/api/email-accounts`

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

- delega a `app.services.email_account_service.list_email_accounts`
- el contrato actual retorna el listado global sin filtrar por usuario
