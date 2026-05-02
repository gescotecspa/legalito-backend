# UC-001 Consultar parametros

## Estado

Borrador

## Objetivo

Permitir consultar el catalogo general de parametros y sus variantes por padre.

## Actores

- cliente consumidor de API
- backend de parametros

## Disparador

El cliente necesita poblar catalogos o filtros dependientes.

## Precondiciones

- existen registros en el catalogo de parametros

## Flujo principal

1. El cliente solicita el listado general o filtrado por `parent_id`.
2. El backend consulta la informacion en la tabla `parameters`.
3. El backend ordena por nombre cuando corresponde.
4. El backend responde la coleccion serializada.

## Flujos alternativos

- Si ocurre un error inesperado de lectura, el flujo responde error tecnico.

## Reglas de negocio

- el filtrado por padre se realiza con `parent_id`
- el listado por padre se ordena por nombre ascendente

## Postcondiciones

- el cliente obtiene el catalogo requerido sin modificar estado

## Criterios de aceptacion

- dado un catalogo existente, cuando se consulta `/api/parameters`, entonces se obtiene la coleccion serializada
- dado un `parent_id` valido, cuando se consulta `/api/parameters/byparent/<parent_id>`, entonces se obtienen solo sus hijos ordenados por nombre
