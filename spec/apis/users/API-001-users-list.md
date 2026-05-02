# API-001 Listar usuarios

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que lista usuarios.

## Endpoint

- metodo: `GET`
- ruta: `/api/users`

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

- delega a `app.services.user_service.list_users`
- no tiene coverage automatizada especifica al momento de este documento
