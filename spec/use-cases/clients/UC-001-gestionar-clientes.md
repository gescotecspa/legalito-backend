# UC-001 Gestionar clientes

## Estado

Implementado

## Objetivo

Permitir que un usuario autenticado administre fichas basicas de clientes propias como base del CRM legal.

## Actores

- usuario autenticado
- backend de clientes

## Disparador

El usuario solicita listar, crear, consultar o actualizar una ficha de cliente.

## Precondiciones

- el usuario esta autenticado

## Flujo principal

1. El usuario solicita una operacion sobre clientes.
2. El backend obtiene la identidad desde JWT.
3. El backend valida los datos minimos cuando corresponde.
4. El backend opera solo sobre clientes cuyo `owner_user` corresponde a la identidad autenticada.
5. El backend responde la ficha o coleccion serializada.

## Flujos alternativos

- Si falta autenticacion, el flujo se rechaza.
- Si falta `name` al crear o actualizar, el flujo se rechaza.
- Si el cliente no existe o pertenece a otro usuario, el flujo devuelve `404`.

## Reglas de negocio

- la identidad del owner sale del JWT
- una ficha de cliente requiere `name`
- el primer corte usa ownership por usuario individual
- la baja/eliminacion de clientes queda fuera del alcance inicial

## Postcondiciones

- el cliente queda disponible para visualizar causas asociadas cuando esa relacion venga desde origen judicial o ingestion validada

## Criterios de aceptacion

- dado un usuario autenticado, cuando lista clientes, obtiene solo sus clientes
- dado un usuario autenticado y payload valido, cuando crea cliente, el cliente queda asociado a su identidad
- dado un cliente ajeno, cuando el usuario intenta consultarlo, obtiene rechazo
- dado un cliente propio, cuando actualiza datos basicos, se persisten los cambios

## Estado de pruebas

- Unit tests: implementado
- Integration tests: parcial
- E2E: pendiente

Escenarios cubiertos:

- validacion de `name`
- creacion con owner desde usuario autenticado
- listado filtrado por owner
- rechazo por ownership
- actualizacion de cliente propio
