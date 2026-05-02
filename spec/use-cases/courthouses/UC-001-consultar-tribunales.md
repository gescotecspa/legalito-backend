# UC-001 Consultar tribunales

## Estado

Borrador

## Objetivo

Permitir consultar el catalogo de tribunales disponibles.

## Actores

- usuario autenticado
- backend de tribunales

## Disparador

El usuario necesita poblar catalogos o filtros asociados a tribunales.

## Precondiciones

- el usuario esta autenticado
- existen registros en la tabla `courthouses`

## Flujo principal

1. El usuario autenticado solicita el listado de tribunales.
2. El backend valida el JWT.
3. El backend consulta la tabla `courthouses`.
4. El backend responde la coleccion serializada.

## Flujos alternativos

- Si el request no esta autenticado, el flujo se rechaza.
- Si ocurre un error inesperado de lectura, el flujo responde error tecnico.

## Reglas de negocio

- el endpoint requiere autenticacion JWT
- el flujo no modifica estado

## Postcondiciones

- el usuario obtiene el catalogo requerido

## Criterios de aceptacion

- dado un usuario autenticado, cuando consulta `/api/courthouses`, entonces obtiene la coleccion serializada
- dado un request sin JWT, cuando consulta `/api/courthouses`, entonces el flujo responde no autenticado
