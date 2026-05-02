# UC-001 Consultar roles

## Estado

Borrador

## Objetivo

Permitir consultar el catalogo de roles disponibles.

## Actores

- cliente consumidor de API
- backend de roles

## Disparador

El cliente necesita poblar permisos, filtros o formularios basados en roles.

## Precondiciones

- existen registros en la tabla `roles`

## Flujo principal

1. El cliente solicita el listado de roles.
2. El backend consulta la tabla `roles`.
3. El backend responde la coleccion serializada.

## Flujos alternativos

- Si ocurre un error inesperado de lectura, el flujo responde error tecnico.

## Reglas de negocio

- el endpoint no modifica estado

## Postcondiciones

- el cliente obtiene el catalogo requerido

## Criterios de aceptacion

- dado un catalogo de roles existente, cuando se consulta `/api/roles`, entonces se obtiene la coleccion serializada
