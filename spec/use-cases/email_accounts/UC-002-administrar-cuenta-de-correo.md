# UC-002 Administrar cuenta de correo

## Estado

Borrador

## Objetivo

Permitir al usuario autenticado consultar, actualizar, activar o eliminar sus cuentas de correo.

## Actores

- usuario autenticado
- backend de cuentas de correo

## Disparador

El usuario necesita mantener la configuracion de una cuenta ya registrada.

## Precondiciones

- el usuario esta autenticado
- la cuenta pertenece al usuario autenticado

## Flujo principal

1. El usuario consulta o modifica una cuenta existente.
2. El backend valida ownership contra la identidad JWT.
3. El backend aplica la accion solicitada.
4. El backend responde el resultado.

## Flujos alternativos

- Si la cuenta no existe o no pertenece al usuario, el flujo se rechaza.
- Si el nuevo correo colisiona con otro existente, el flujo se rechaza.

## Reglas de negocio

- las operaciones por id respetan ownership estricto
- el cambio de `email_address` no puede colisionar con otra cuenta

## Postcondiciones

- la cuenta queda actualizada, activada/desactivada o eliminada segun corresponda

## Criterios de aceptacion

- dado un usuario autenticado y una cuenta propia, cuando actualiza o consulta la cuenta, entonces el backend respeta ownership y devuelve el resultado esperado
