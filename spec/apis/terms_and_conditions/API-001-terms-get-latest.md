# API-001 Obtener ultima version de terminos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna la ultima version disponible de terminos y condiciones.

## Endpoint

- metodo: `GET`
- ruta: `/api/terms`

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
{
  "id": 1,
  "version": "v1",
  "content": "Terminos",
  "created_at": "2026-05-01T10:00:00"
}
```

## Errores esperados

- `404`: no existen terminos registrados

## Notas tecnicas

- delega a `app.services.terms_and_conditions_service.TermsAndConditionsService.get_latest_version`
