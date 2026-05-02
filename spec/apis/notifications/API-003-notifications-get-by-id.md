# API-003 Obtener notificacion por id

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna una notificacion puntual respetando ownership.

## Endpoint

- metodo: `GET`
- ruta: `/api/notifications/<id>`

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
{
  "id": 7
}
```

## Errores esperados

- `401`: no autenticado
- `404`: notificacion inexistente o fuera del ownership del usuario autenticado
- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.notification_service.get_notification`
- usa el `user` del JWT para restringir la consulta
- tiene coverage automatizada basica de ownership
