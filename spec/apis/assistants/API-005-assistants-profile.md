# API-005 Obtener perfil de asistente

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que obtiene el perfil de un asistente por id.

## Endpoint

- metodo: `GET`
- ruta: `/api/assistants/profile/<id>`

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
{}
```

## Errores esperados

- `401`: no autenticado
- `404`: asistente no encontrado

## Notas tecnicas

- delega a `app.services.assistant_service.get_assistant_service`
- tiene coverage automatizada basica del caso exitoso
