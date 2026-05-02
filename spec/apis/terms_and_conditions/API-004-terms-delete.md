# API-004 Eliminar terminos por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina una version de terminos.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/terms/<terms_id>`

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
  "message": "Terms and conditions with ID 2 deleted"
}
```

## Errores esperados

- `401`: no autenticado
- `404`: terminos inexistentes

## Notas tecnicas

- delega a `TermsAndConditionsService.delete_terms`
