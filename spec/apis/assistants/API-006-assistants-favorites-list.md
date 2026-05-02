# API-006 Listar asistentes favoritos

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista asistentes marcados como favoritos por el usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/assistants/favorites`

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
- `400`: falta identidad de usuario

## Notas tecnicas

- usa la identidad JWT y no confia en un `user` enviado en request
- delega a `app.services.assistant_service.list_assistants_favorite_service`
- tiene coverage automatizada de uso de JWT
