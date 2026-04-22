# Dominio

## Resumen

Este backend expone una API Flask para operaciones de autenticacion, administracion de usuarios y entidades de apoyo a la gestion juridica.

## Capacidades detectadas en el repo

- autenticacion y recuperacion de contraseña
- gestion de usuarios
- gestion de asistentes
- gestion de causas
- gestion de folios
- gestion de notificaciones
- gestion de parametros
- gestion de roles
- gestion de tribunales
- lectura de correos externos por IMAP
- administracion de cuentas de correo asociadas a usuarios
- creacion y envio de eventos con adjunto `.ics`
- administracion de terminos y condiciones
- carga de imagenes

## Actores principales

- usuario autenticado
- usuario no autenticado en flujo de login, registro o recuperacion
- servicios externos de correo
- proveedor SMTP para invitaciones de calendario
- proveedor Mailjet para correos transaccionales

## Observaciones actuales

- la API se organiza por blueprints bajo prefijo `/api`
- la persistencia usa SQLAlchemy con migraciones Alembic
- existe integracion con JWT para autenticacion
- hay integraciones externas de correo separadas segun caso de uso
- no se detecto aun una carpeta de especificacion previa, por lo que esta base nace como punto inicial

## Navegacion recomendada

- usar este archivo para entender el dominio general
- usar `context/system-map.md` para ubicar modulos, endpoints e integraciones
- usar `apis/` y `use-cases/` por dominio para documentar cambios concretos
