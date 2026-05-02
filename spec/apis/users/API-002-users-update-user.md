# API-002 Actualizar usuario

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que actualiza campos permitidos de un usuario.

## Endpoint

- metodo: `PUT`
- ruta: `/api/users/<user>`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "first_name": "Ada",
  "last_name": "Lovelace",
  "phone_number": "+56911111111",
  "birth_date": "1990-01-01T00:00:00"
}
```

## Response esperada

### Exito

```json
{}
```

## Errores esperados

- `401`: no autenticado
- `404`: usuario no encontrado

## Notas tecnicas

- delega a `app.services.user_service.update_user`
- permite actualizar `first_name`, `last_name`, `phone_number`, `birth_date` e imagen via `image_base64`
- no tiene coverage automatizada especifica al momento de este documento
