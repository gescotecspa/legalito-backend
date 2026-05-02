# API-002 Filtrar asistentes

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que filtra asistentes por tipo y region.

## Endpoint

- metodo: `GET`
- ruta: `/api/assistants/filter/<typeId>/<regionId>`

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
- `404`: filtro sin resultados si el servicio decide tratarlo como no encontrado

## Notas tecnicas

- delega a `app.services.assistant_service.list_assistants_by_filter_service`
- permite usar `0` como comodin para tipo o region
- falta coverage automatizada especifica
