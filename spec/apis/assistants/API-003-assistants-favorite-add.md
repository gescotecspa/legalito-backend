# API-003 Agregar asistente a favoritos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que agrega un asistente a favoritos del usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/assistants/favorite/add`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{
  "assistantId": 12
}
```

## Response esperada

### Exito

```json
true
```

## Errores esperados

- `400`: falta `assistantId`
- `401`: no autenticado
- `404`: asistente no encontrado

## Notas tecnicas

- usa la identidad JWT y no confia en un `user` del body
- delega a `app.services.assistant_service.add_favorite_assistant_service`
- tiene coverage automatizada de `401`, `400`, `404` y uso de JWT
