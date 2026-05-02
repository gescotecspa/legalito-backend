# API-001 Crear folio

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que crea un folio asociado a una causa.

## Endpoint

- metodo: `POST`
- ruta: `/api/folios`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "case_id": 1,
  "folio_number": "F-001",
  "description": "Descripcion opcional"
}
```

## Response esperada

### Exito

```json
{
  "message": "Folio created successfully.",
  "folio": {}
}
```

## Errores esperados

- `400`: faltan `case_id` o `folio_number`
- `400`: la causa asociada no existe
- `401`: no autenticado

## Notas tecnicas

- delega a `app.services.folio_service.create_folio_service`
- valida que la causa exista antes de persistir el folio
- tiene coverage automatizada basica para el servicio y el endpoint
