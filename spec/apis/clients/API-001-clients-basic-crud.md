# API-001 Clients Basic CRUD

## Estado

Implementado

## Objetivo

Describir los endpoints basicos de clientes para el primer corte CRM legal.

## Autenticacion

Requiere `Bearer token` en todos los endpoints.

## Endpoints

### `GET /api/clients`

Lista clientes cuyo `owner_user` corresponde al JWT.

Respuesta exitosa `200`:

```json
[
  {
    "id": 1,
    "owner_user": "user@example.com",
    "name": "Cliente Demo",
    "identification": "11.111.111-1",
    "email": "cliente@example.com",
    "phone_number": "+56912345678",
    "address": "Direccion",
    "notes": "Notas",
    "status": "active",
    "created_at": "2026-07-24T22:30:00",
    "updated_at": "2026-07-24T22:30:00"
  }
]
```

### `POST /api/clients`

Crea un cliente asociado al JWT. El backend ignora cualquier intento de forjar owner desde el body.

Request:

```json
{
  "name": "Cliente Demo",
  "identification": "11.111.111-1",
  "email": "cliente@example.com",
  "phone_number": "+56912345678",
  "address": "Direccion",
  "notes": "Notas"
}
```

Respuesta exitosa `201`: ficha serializada.

### `GET /api/clients/<client_id>`

Obtiene ficha de cliente propio, incluyendo causas asociadas cuando existan.

Respuesta exitosa `200`: ficha serializada con `cases`.

### `PUT /api/clients/<client_id>`

Actualiza datos basicos de cliente propio.

Respuesta exitosa `200`: ficha serializada.

## Errores esperados

- `400`: datos invalidos o falta `name`
- `401`: falta autenticacion
- `404`: cliente inexistente o fuera del ownership
- `500`: error inesperado

## Notas tecnicas

- `owner_user` se obtiene desde JWT.
- el primer corte no incluye eliminacion de clientes.
- `Case.serialize()` expone `client_id` y `client` cuando existe asociacion proveniente de origen judicial, ingestion validada o proceso backend autorizado.

## Estado de pruebas

- Unit tests: implementado
- Integration tests: parcial
- E2E: pendiente

Cobertura actual:

- `GET /clients` requiere JWT y usa identidad autenticada
- `POST /clients` usa identidad autenticada
- `GET /clients/<id>` rechaza cliente fuera de ownership
- servicios cubren creacion, listado, ownership y actualizacion
