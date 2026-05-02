# API-002 Listar causas por usuario autenticado

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista causas asociadas al usuario autenticado.

## Endpoint

- metodo: `POST`
- ruta: `/api/cases/byUser`

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

- `400`: falta identidad de usuario
- `401`: no autenticado

## Notas tecnicas

- usa `get_jwt_identity()` y no confia en `user` del body
- delega a `app.services.case_service.list_cases_by_user_service`
- tiene coverage automatizada de uso de JWT y rechazo a request sin autenticacion
