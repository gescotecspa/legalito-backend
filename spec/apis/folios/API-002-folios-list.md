# API-002 Listar folios

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista folios.

## Endpoint

- metodo: `GET`
- ruta: `/api/folios`

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
[]
```

## Errores esperados

- `401`: no autenticado

## Notas tecnicas

- delega a `app.services.folio_service.list_folios_service`
- devuelve folios serializados
- tiene coverage automatizada basica del endpoint
