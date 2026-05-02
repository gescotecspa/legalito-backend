# API-001 Crear causa

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que crea una causa.

## Endpoint

- metodo: `POST`
- ruta: `/api/cases`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "rit": "RIT-001",
  "name": "Caso principal",
  "status": "active"
}
```

## Response esperada

### Exito

```json
{
  "message": "Case created successfully.",
  "case": {}
}
```

## Errores esperados

- `400`: faltan `rit` o `name`
- `401`: no autenticado
- `409`: ya existe una causa con el mismo `rit`

## Notas tecnicas

- delega a `app.services.case_service.create_case`
- persiste una causa nueva con `created_at`
- falta coverage automatizada especifica de este endpoint
