# API-003 Actualizar terminos por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que actualiza una version de terminos existente.

## Endpoint

- metodo: `PUT`
- ruta: `/api/terms/<terms_id>`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "content": "Terminos actualizados",
  "version": "v2"
}
```

## Response esperada

### Exito

```json
{
  "id": 2,
  "version": "v2",
  "content": "Terminos actualizados"
}
```

## Errores esperados

- `400`: faltan `content` o `version`
- `401`: no autenticado
- `404`: terminos inexistentes o fallo de update

## Notas tecnicas

- delega a `TermsAndConditionsService.update_terms`
