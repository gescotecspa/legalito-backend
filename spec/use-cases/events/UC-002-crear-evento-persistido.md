# UC-002 Crear evento persistido

## Estado

Borrador

## Objetivo

Permitir que un usuario autenticado cree un evento persistido asociado a su cuenta.

## Actores

- usuario autenticado
- backend de eventos

## Disparador

El usuario registra un evento propio desde la aplicacion.

## Precondiciones

- el usuario esta autenticado
- se informan `title` y `start_date`

## Flujo principal

1. El usuario envia titulo, fecha de inicio y datos opcionales del evento.
2. El backend toma la identidad desde JWT.
3. El backend valida formato de fecha y existencia del usuario autenticado.
4. Si se informa `type_id`, el backend valida que exista.
5. El backend persiste el evento.
6. El backend responde el evento creado.

## Flujos alternativos

- Si faltan `title` o `start_date`, el flujo se rechaza por validacion.
- Si la fecha no tiene formato valido, el flujo se rechaza.
- Si el usuario autenticado no existe en base, el flujo se rechaza.
- Si `type_id` no existe, el flujo se rechaza.

## Reglas de negocio

- el owner del evento debe ser el usuario autenticado
- `type_id` es opcional

## Postcondiciones

- en caso exitoso, el evento queda persistido para el usuario autenticado

## Criterios de aceptacion

- dado un request valido, cuando el usuario esta autenticado, entonces el evento se crea
- dado un `type_id` inexistente, cuando se procesa el request, entonces el flujo devuelve error de validacion
