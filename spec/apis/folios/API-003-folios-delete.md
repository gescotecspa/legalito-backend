# API-003 Eliminar folio

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina un folio por id.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/folios/<folio_id>`

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
  "message": "Folio deleted successfully."
}
```

## Errores esperados

- `401`: no autenticado
- `404`: folio no encontrado

## Notas tecnicas

- delega a `app.services.folio_service.delete_folio_service`
- tiene coverage automatizada basica para `404`
