# UC-002 Descartar notificacion

## Estado

Borrador

## Objetivo

Permitir al usuario autenticado marcar una notificacion como descartada.

## Actores

- usuario autenticado
- backend de notificaciones

## Disparador

El usuario decide ocultar una notificacion ya revisada.

## Precondiciones

- el usuario esta autenticado
- la notificacion pertenece al usuario

## Flujo principal

1. El usuario envia el `id` de la notificacion.
2. El backend obtiene la identidad desde JWT.
3. El backend busca la notificacion del usuario.
4. El backend cambia el estado a `dismissed`.
5. El backend responde confirmacion.

## Flujos alternativos

- Si la notificacion no existe o no pertenece al usuario, el flujo se rechaza.

## Reglas de negocio

- solo puede descartarse una notificacion propia
- descartar no elimina el registro, solo cambia el estado

## Postcondiciones

- la notificacion queda marcada como `dismissed`

## Criterios de aceptacion

- dado un usuario autenticado y una notificacion propia, cuando solicita descartarla, entonces el backend actualiza su estado a `dismissed`
