# API-002 Listar parametros por padre

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna parametros filtrados por `parent_id`.

## Endpoint

- metodo: `GET`
- ruta: `/api/parameters/byparent/<parent_id>`

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
    "id": 2,
    "parent_id": 1,
    "name": "Activo",
    "description": "Estado activo",
    "created_at": "2026-05-01T10:00:00"
  }
]
```

## Errores esperados

- `404`: no se encuentra el recurso asociado si el servicio lo declara asi
- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.parameter_service.list_parameters_by_parent_service`
- ordena por `Parameter.name` ascendente
- tiene coverage automatizada basica del servicio y del endpoint
