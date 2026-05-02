# API-002 Obtener cuenta de correo por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que obtiene una cuenta de correo asociada al usuario autenticado.

## Endpoint

- metodo: `GET`
- ruta: `/api/email-accounts/<id>`

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
{
  "id": 1,
  "provider": "gmail",
  "imap_server": "imap.gmail.com",
  "email_address": "account@example.com",
  "active": true,
  "user": "owner@example.com"
}
```

## Errores esperados

- `401`: no autenticado
- `404`: cuenta no encontrada o no pertenece al usuario

## Notas tecnicas

- valida ownership con `get_email_account_by_id_for_user`
- la serializacion ya no expone `password`
- tiene cobertura automatizada para acceso a cuenta ajena
