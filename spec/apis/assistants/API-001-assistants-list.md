# API-001 Listar asistentes

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista asistentes.

## Endpoint

- metodo: `GET`
- ruta: `/api/assistants`

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

- delega a `app.services.assistant_service.list_assistants_service`
- devuelve asistentes serializados
- falta coverage automatizada especifica
