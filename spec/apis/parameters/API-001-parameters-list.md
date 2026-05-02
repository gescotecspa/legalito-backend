# API-001 Listar parametros

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna el catalogo general de parametros.

## Endpoint

- metodo: `GET`
- ruta: `/api/parameters`

## Autenticacion

- publica

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
    "parent_id": null,
    "name": "Estado",
    "description": "Catalogo padre",
    "created_at": "2026-05-01T10:00:00"
  }
]
```

## Errores esperados

- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.parameter_service.list_parameters_service`
- serializa el modelo `Parameter` sin transformaciones adicionales
- tiene coverage automatizada basica del servicio y del endpoint
