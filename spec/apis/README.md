# APIs

Esta carpeta documenta contratos tecnicos de endpoints.

## Organizacion

Los specs deben agruparse por dominio funcional. Ejemplos:

- `auth/`
- `users/`
- `cases/`
- `clients/`
- `tasks/`
- `mails/`
- `events/`

## Cuando agregar un spec de API

- se crea un endpoint
- cambia request, response o errores
- cambia autenticacion o autorizacion

## Nombres sugeridos

- `auth/API-001-auth-register.md`
- `auth/API-002-auth-forgot-password.md`

## Tareas asociadas

Si hace falta seguimiento operativo, crear un archivo hermano con sufijo `.tasks.md`.
