# API-005 Eliminar evento propio

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que elimina un evento perteneciente al usuario autenticado.

## Endpoint

- metodo: `DELETE`
- ruta: `/api/events/delete/<event_id>`

## Autenticacion

- protegida con JWT

## Request

### Path params

- `event_id`: identificador del evento a eliminar

## Response esperada

### Exito

```json
{
  "message": "Evento eliminado exitosamente"
}
```

## Errores esperados

- `401`: no autenticado
- `500`: el evento no existe o no pertenece al usuario

## Notas tecnicas

- usa `get_jwt_identity()` para resolver ownership
- delega a `app.services.event_service.delete_event_service`
- el servicio hoy devuelve `ValueError` cuando no encuentra el evento o el ownership no coincide
- el blueprint actual no diferencia ese caso y responde `500`; conviene corregirlo en implementacion futura
