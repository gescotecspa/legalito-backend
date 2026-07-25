# UC-001 Gestionar tareas

## Estado

Implementado

## Objetivo

Permitir que un usuario autenticado gestione tareas operativas propias, opcionalmente vinculadas a una causa o cliente visible.

## Actores

- usuario autenticado
- backend de tareas

## Disparador

El usuario solicita listar, crear, consultar, actualizar o completar una tarea.

## Precondiciones

- el usuario esta autenticado
- si se informa `case_id`, la causa pertenece al usuario
- si se informa `client_id`, el cliente pertenece al usuario

## Flujo principal

1. El usuario solicita una operacion sobre tareas.
2. El backend obtiene la identidad desde JWT.
3. El backend valida titulo, estado, prioridad y vinculos opcionales.
4. El backend opera solo sobre tareas cuyo `owner_user` corresponde a la identidad autenticada.
5. El backend responde la tarea o coleccion serializada.

## Flujos alternativos

- Si falta autenticacion, el flujo se rechaza.
- Si falta `title` al crear o actualizar, el flujo se rechaza.
- Si la causa o cliente asociado no pertenece al usuario, el flujo se rechaza.
- Si la tarea no existe o pertenece a otro usuario, el flujo devuelve `404`.

## Reglas de negocio

- la identidad del owner sale del JWT
- una tarea requiere `title`
- estados permitidos: `pending`, `in_progress`, `completed`, `cancelled`
- prioridades permitidas: `low`, `normal`, `high`, `urgent`
- completar una tarea no elimina su historial

## Postcondiciones

- la tarea queda disponible para listados generales o secciones de causa/cliente

## Criterios de aceptacion

- dado un usuario autenticado, cuando lista tareas, obtiene solo sus tareas
- dado un payload valido, cuando crea tarea, queda asociada al usuario autenticado
- dado un vinculo a causa o cliente ajeno, el flujo se rechaza
- dado una tarea propia, cuando la completa, queda con estado `completed`

## Estado de pruebas

- Unit tests: implementado
- Integration tests: parcial
- E2E: pendiente

Escenarios cubiertos:

- validacion de `title`
- creacion con owner desde JWT
- validacion de ownership para causa y cliente
- listado filtrado por owner
- rechazo por ownership de tarea
- actualizacion de estado/prioridad
- completado de tarea

