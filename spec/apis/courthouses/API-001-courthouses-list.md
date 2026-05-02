# API-001 Listar tribunales

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna el catalogo de tribunales.

## Endpoint

- metodo: `GET`
- ruta: `/api/courthouses`

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
  {
    "id": 1,
    "name": "Juzgado Civil",
    "type_id": 1,
    "address": "Calle 123",
    "phone_number": "1234567",
    "email": "court@example.com",
    "website": "https://court.example.com",
    "status": "active",
    "created_at": "2026-05-01T10:00:00",
    "updated_at": "2026-05-01T10:00:00"
  }
]
```

## Errores esperados

- `401`: no autenticado
- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.courthouse_service.list_courthouses_service`
- serializa el modelo `Courthouse` sin transformaciones adicionales
- tiene coverage automatizada basica del servicio y del endpoint
