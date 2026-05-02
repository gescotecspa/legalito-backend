# UC-001 Consultar notificaciones activas

## Estado

Borrador

## Objetivo

Permitir al usuario autenticado consultar sus notificaciones activas.

## Actores

- usuario autenticado
- backend de notificaciones

## Disparador

El usuario abre la bandeja de notificaciones.

## Precondiciones

- el usuario esta autenticado
- existen notificaciones asociadas al usuario

## Flujo principal

1. El usuario solicita sus notificaciones.
2. El backend obtiene la identidad desde JWT.
3. El backend consulta notificaciones activas del usuario.
4. El backend responde la coleccion serializada.

## Flujos alternativos

- Si el request no esta autenticado, el flujo se rechaza.

## Reglas de negocio

- solo se devuelven notificaciones del usuario autenticado
- el flujo principal de consulta por usuario filtra por `status = active`

## Postcondiciones

- el usuario obtiene su bandeja actual sin modificar estado

## Criterios de aceptacion

- dado un usuario autenticado con notificaciones activas, cuando consulta el endpoint por usuario, entonces obtiene solo sus notificaciones
