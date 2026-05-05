# UC-002 Aceptar ultima version de terminos

## Estado

Borrador

## Objetivo

Permitir al usuario autenticado aceptar la ultima version disponible de terminos y condiciones.

## Actores

- usuario autenticado
- backend de terminos y condiciones

## Disparador

El usuario acepta la version vigente desde la aplicacion.

## Precondiciones

- el usuario esta autenticado
- existe al menos una version de terminos publicada
- el usuario existe en la base

## Flujo principal

1. El usuario solicita aceptar terminos.
2. El backend obtiene la identidad desde JWT.
3. El backend recibe `terms_id` desde el cliente.
4. El backend busca la ultima version publicada.
5. El backend valida que `terms_id` coincida con la version vigente.
6. El backend actualiza el usuario con esa referencia.
7. El backend responde el usuario actualizado.

## Flujos alternativos

- Si el usuario no existe, el flujo se rechaza.
- Si no hay terminos disponibles, el flujo se rechaza.
- Si `terms_id` no coincide con la version vigente, el flujo se rechaza.

## Reglas de negocio

- siempre se asocia la ultima version disponible
- el usuario aceptante se obtiene solo desde JWT
- el cliente debe informar el `terms_id` que esta aceptando
- el backend solo acepta la operacion si ese `terms_id` corresponde a la version vigente

## Postcondiciones

- el usuario queda asociado a la ultima version de terminos

## Criterios de aceptacion

- dado un usuario autenticado y el `terms_id` vigente, cuando acepta terminos, entonces su registro queda asociado a la ultima version
- dado un `terms_id` desactualizado, cuando intenta aceptar terminos, entonces el flujo devuelve conflicto
