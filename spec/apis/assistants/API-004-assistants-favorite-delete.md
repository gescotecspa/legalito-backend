# API-004 Eliminar asistente de favoritos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina un asistente de favoritos del usuario autenticado.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/assistants/favorite/delete`

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
- `404`: favorito no encontrado

## Notas tecnicas

- delega a `app.services.assistant_service.delete_favorite_assistant_service`
- tiene coverage automatizada basica de `404`
