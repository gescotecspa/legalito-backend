# Testing

## Objetivo

Mantener una estrategia minima de pruebas para refactors de arquitectura, especialmente en auth, persistencia e integraciones externas.

## Estrategia minima

- Unit tests para servicios con reglas o validaciones propias.
- Tests de controller/blueprint para validar status codes, errores y shape basico de respuesta.
- Dobles livianos para integraciones externas: Mailjet, SMTP e IMAP no deben ejecutarse contra proveedores reales en pruebas automatizadas.
- Validacion manual trazable para flujos que dependen de correo real, calendario o credenciales externas.

## Prioridad inicial

1. `auth`: login, recuperacion de contraseña por codigo, cambio de contraseña y cuenta inactiva.
2. `mails`: lectura IMAP con doble, creacion de notificacion y deteccion de invitacion.
3. `events`: generacion/envio de invitacion `.ics` con SMTP fake.
4. `bootstrap`: app factory sin escritura implicita y comando explicito de setup.

## Criterio para refactors

Antes de tocar un flujo sensible, cubrir al menos:

- caso exitoso principal
- campos requeridos
- error esperado de dominio
- integracion externa reemplazada por doble

Si no existe suite automatizada disponible en el entorno, dejar registrada la validacion manual minima en el task operativo correspondiente.
