# API-005 Aceptar ultima version de terminos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que marca al usuario autenticado con la ultima version de terminos disponible.

## Endpoint

- metodo: `PUT`
- ruta: `/api/users/<user_id>/accept-terms`

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
  "user": "owner@example.com",
  "terms_and_conditions": {}
}
```

## Errores esperados

- `401`: no autenticado
- `404`: usuario inexistente
- `409`: no hay terminos disponibles
- `500`: error inesperado

## Notas tecnicas

- delega a `TermsAndConditionsService.accept_terms`
- ignora el `user_id` de la ruta y usa la identidad JWT
- tiene coverage automatizada basica para `401`, `404`, `409` y uso de identidad autenticada
