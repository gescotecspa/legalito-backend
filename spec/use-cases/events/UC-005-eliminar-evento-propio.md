# UC-005 Eliminar evento propio

## Estado

Borrador

## Objetivo

Permitir que un usuario autenticado elimine un evento que le pertenece.

## Actores

- usuario autenticado
- backend de eventos

## Disparador

El usuario decide borrar un evento persistido.

## Precondiciones

- el usuario esta autenticado
- el evento existe y pertenece al usuario

## Flujo principal

1. El usuario solicita eliminar el evento.
2. El backend toma la identidad desde JWT.
3. El backend valida ownership del evento.
4. El backend elimina el registro.
5. El backend responde confirmacion.

## Flujos alternativos

- Si el evento no existe o no pertenece al usuario, el flujo se rechaza.

## Reglas de negocio

- no se permite eliminar eventos ajenos

## Postcondiciones

- en caso exitoso, el evento deja de existir en la base

## Criterios de aceptacion

- dado un evento propio, cuando el usuario lo elimina, entonces el backend responde confirmacion
