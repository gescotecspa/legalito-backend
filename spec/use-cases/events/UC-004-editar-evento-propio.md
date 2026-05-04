# UC-004 Editar evento propio

## Estado

Borrador

## Objetivo

Permitir que un usuario autenticado actualice un evento que le pertenece.

## Actores

- usuario autenticado
- backend de eventos

## Disparador

El usuario modifica datos de un evento ya registrado.

## Precondiciones

- el usuario esta autenticado
- el evento existe y pertenece al usuario

## Flujo principal

1. El usuario envia los campos a actualizar.
2. El backend toma la identidad desde JWT.
3. El backend valida ownership del evento.
4. El backend valida fecha o tipo de evento si esos campos fueron informados.
5. El backend persiste los cambios.
6. El backend responde el evento actualizado.

## Flujos alternativos

- Si el evento no existe o no pertenece al usuario, el flujo se rechaza.
- Si la fecha tiene formato invalido, el flujo se rechaza.
- Si `type_id` no existe, el flujo se rechaza.

## Reglas de negocio

- solo se actualizan los campos efectivamente enviados
- no se permite editar eventos ajenos

## Postcondiciones

- en caso exitoso, el evento queda actualizado

## Criterios de aceptacion

- dado un evento propio y un request valido, cuando el usuario lo edita, entonces los cambios quedan persistidos
- dado un evento ajeno, cuando el usuario intenta editarlo, entonces el flujo devuelve error
