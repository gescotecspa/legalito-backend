# API-006 Obtener cuenta de correo por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna una cuenta puntual respetando ownership.

## Endpoint

- metodo: `GET`
- ruta: `/api/email-accounts/<id>`

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
- `404`: cuenta inexistente o fuera del ownership del usuario autenticado

## Notas tecnicas

- delega a `app.services.email_account_service.get_email_account_by_id_for_user`
- tiene coverage automatizada basica de ownership
