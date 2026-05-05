# API-005 Aceptar ultima version de terminos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que marca al usuario autenticado con la ultima version vigente de terminos, validando el `terms_id` recibido desde el cliente.

## Endpoint

- metodo: `PUT`
- ruta: `/api/terms/accept`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "terms_id": 2
}
```

## Response esperada

### Exito

```json
{
  "user": "owner@example.com",
  "terms_and_conditions": {}
}
```

## Errores esperados

- `400`: falta `terms_id`
- `401`: no autenticado
- `404`: usuario inexistente
- `409`: no hay terminos disponibles
- `409`: `terms_id` no corresponde a la ultima version vigente
- `500`: error inesperado

## Notas tecnicas

- delega a `TermsAndConditionsService.accept_terms`
- usa la identidad JWT como unica fuente de usuario
- exige `terms_id` en el body para validar que el cliente este aceptando la version vigente visible en frontend
- tiene coverage automatizada basica para `401`, `404`, `409` y uso de identidad autenticada
