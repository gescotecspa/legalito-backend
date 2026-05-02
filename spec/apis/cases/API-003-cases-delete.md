# API-003 Eliminar causa

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina una causa por id.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/cases/<case_id>`

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
  "message": "Case deleted successfully."
}
```

## Errores esperados

- `401`: no autenticado
- `404`: causa no encontrada

## Notas tecnicas

- delega a `app.services.case_service.delete_case_service`
- tiene coverage automatizada basica para `404`
