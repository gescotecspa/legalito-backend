# API-002 Crear terminos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que crea una nueva version de terminos.

## Endpoint

- metodo: `POST`
- ruta: `/api/terms`

## Autenticacion

- publica segun implementacion actual

## Request

### Body

```json
{
  "content": "Terminos de uso",
  "version": "v2"
}
```

## Response esperada

### Exito

```json
{
  "id": 2,
  "version": "v2",
  "content": "Terminos de uso"
}
```

## Errores esperados

- `400`: faltan `content` o `version`

## Notas tecnicas

- el contrato actual se publica desde `TermsAndConditionsListResource.post`
- la falta de autenticacion en este endpoint merece revision posterior
