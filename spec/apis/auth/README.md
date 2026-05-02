# APIs Auth

Specs de contratos HTTP para login, registro, recuperacion de contraseña y otros endpoints de autenticacion.

## Estado de pruebas

- Unit tests: implementados para flujos principales y mapeo HTTP critico
- Integration tests: pendiente
- E2E: pendiente

## Cobertura actual

- validacion de request incompleto en `login` y `reset-password`
- mapeo HTTP de `InvalidCredentialsException` a `401`
- mapeo HTTP de `InactiveAccountException` a `403`
- mapeo HTTP de rate limiting a `429` en `login`, `forgot-password` y `reset-password`
- validacion de request no JSON en `register`
- mapeo HTTP de conflictos en `register`
- mapeo HTTP de errores de recuperacion de contraseña en `forgot-password` y `reset-password`
- mapeo HTTP de fallo de entrega de correo en `forgot-password` a `502`

## Validacion manual actual

- en dev: `register` y `login` funcionan sobre base recreada
- en QA: `health`, `register` y `login` quedaron validados con respuesta exitosa
- en QA: `forgot-password` devuelve `502`, consistente con el fallo real del proveedor de correo

## Observaciones abiertas

- Mailjet ya no esta disponible como proveedor efectivo de envio en QA
- el siguiente ajuste funcional en `auth` es reemplazar Mailjet por otro proveedor o por SMTP directo
