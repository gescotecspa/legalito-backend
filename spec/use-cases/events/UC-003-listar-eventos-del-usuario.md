# UC-003 Listar eventos del usuario

## Estado

Borrador

## Objetivo

Permitir que un usuario autenticado consulte sus eventos persistidos.

## Actores

- usuario autenticado
- backend de eventos

## Disparador

El usuario solicita ver sus eventos.

## Precondiciones

- el usuario esta autenticado

## Flujo principal

1. El usuario solicita el listado de eventos.
2. El backend toma la identidad desde JWT.
3. El backend busca los eventos asociados a ese usuario.
4. El backend ordena los resultados por fecha de inicio ascendente.
5. El backend responde la lista.

## Flujos alternativos

- Si falta identidad de usuario, el flujo se rechaza.

## Reglas de negocio

- la identidad del JWT prevalece sobre cualquier valor `user` enviado en el body
- solo se listan eventos del usuario autenticado

## Postcondiciones

- el usuario recibe su lista actual de eventos

## Criterios de aceptacion

- dado un usuario autenticado con eventos, cuando solicita el listado, entonces recibe solo sus eventos ordenados por fecha
