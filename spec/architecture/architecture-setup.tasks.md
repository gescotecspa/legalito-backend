# TASKS Setup de arquitectura del backend

## Estado general

Cerrado a nivel de arquitectura base. Quedan follow-ups operativos e integraciones por validar o reemplazar.

## Objetivo

Ordenar el backend antes de seguir agregando funcionalidades, reduciendo mezcla de capas, side effects en arranque y acoplamientos entre API, servicios, modelos e integraciones.

## Alcance

Este plan cubre ajustes estructurales y tecnicos del backend actual.

No define nuevas reglas de negocio ni contratos API nuevos.

## Hallazgos base que motivan este plan

- el app factory ejecuta efectos colaterales de base de datos en el arranque
- los blueprints contienen logica de aplicacion, validaciones y persistencia directa
- algunos modelos contienen commits o exponen datos sensibles al serializar
- hay logica de integracion externa viviendo en `utils/`
- existen servicios con responsabilidades mezcladas o caminos funcionales duplicados

## Orden sugerido

1. estabilizar bootstrap y setup operativo
2. refactorizar vertical `auth`
3. separar integraciones externas
4. ordenar servicios por responsabilidad
5. cerrar con pruebas, validacion manual y documentacion

## Checklist

- [x] validar este plan como guia de trabajo
- [x] definir si hace falta ADR para la arquitectura objetivo o si basta con este plan operativo
- [x] sacar `db.create_all()` del app factory
- [x] sacar `initialize_statuses()` del arranque HTTP y moverlo a un setup explicito
- [x] definir mecanismo de setup inicial del entorno local y no productivo
- [x] documentar el flujo de arranque esperado en `spec/architecture/overview.md` o artefacto asociado
- [x] consolidar el flujo de login en una capa de servicio consistente
- [x] mover `forgot-password` a un servicio de caso de uso
- [x] mover `reset-password` a un servicio de caso de uso
- [x] eliminar acceso directo a modelos y commits desde `app/api/auth.py`
- [x] decidir y documentar un unico enfoque de recuperacion de contraseña
- [x] quitar commits desde modelos como `User`
- [x] evitar serializacion de datos sensibles como `password_hash` y `reset_code`
- [x] mover SMTP, IMAP y mailers a una capa de integraciones explicita
- [x] definir criterio de uso para `services/` vs `integrations/` vs `utils/`
- [x] separar servicios grandes o mezclados por responsabilidad
- [x] reemplazar `print` por logging consistente en flujos sensibles
- [x] definir estrategia minima de pruebas para refactors de arquitectura
- [ ] validar manualmente login, registro, recuperacion de contraseña, lectura de mails y envio de eventos
- [x] validar tecnicamente recreacion completa de base vacia con migraciones y setup inicial
- [x] dejar actualizado `spec/context/system-map.md` si cambian modulos o ubicaciones
- [x] cerrar el plan con resumen de cambios, riesgos residuales y proximos pasos

## Fases sugeridas

## Fase 1. Bootstrap y setup

Objetivo: que el arranque HTTP no modifique estado operativo por defecto.

Entregables:

- app factory sin side effects de inicializacion de datos
- mecanismo explicito de setup o bootstrap
- documentacion minima del flujo de arranque

## Fase 2. Vertical Auth

Objetivo: usar `auth` como primer vertical para consolidar el patron `api -> service -> model/integration`.

Entregables:

- blueprints mas delgados
- servicios de auth y password reset consistentes
- eliminacion de caminos funcionales duplicados

## Fase 3. Integraciones externas

Objetivo: hacer visibles y testeables las integraciones con correo y calendario.

Entregables:

- estructura clara para Mailjet, SMTP e IMAP
- responsabilidades movidas fuera de `utils/`
- configuracion y errores mas faciles de trazar

## Fase 4. Saneamiento transversal

Objetivo: homogeneizar patrones del resto del backend.

Entregables:

- servicios separados por responsabilidad
- reglas claras para serializacion
- logging mas consistente

## Dependencias y decisiones a confirmar

- si se desea crear una carpeta nueva `app/integrations/` o mantener integraciones dentro de `app/services/`
- si el setup inicial debe resolverse con comando Flask, script dedicado o proceso de deployment
- si el flujo de recuperacion de contraseña quedara con codigo temporal o volvera a token

## Riesgos

- mover bootstrap sin un mecanismo alternativo puede romper ambientes nuevos
- refactorizar `auth` sin pruebas puede introducir regresiones de acceso
- tocar integraciones de correo sin validacion manual puede romper flujos silenciosamente
- seguir refactorizando sin cerrar una estructura objetivo puede mover el desorden de carpeta

## Validacion manual minima al cierre

- registro de usuario
- login con usuario activo
- recuperacion de contraseña
- cambio de contraseña con flujo vigente
- lectura de correos asociados
- generacion y envio de invitacion `.ics`

Estado: parcialmente ejecutada. `auth` y bootstrap ya fueron validados en dev y QA; quedan pendientes `mails` y `events`.

## Resumen de cierre

- el app factory ya no crea esquema ni carga datos base al arrancar HTTP
- el setup inicial queda disponible mediante comando Flask explicito
- `auth` queda organizado como `api -> service -> model/integration`
- el flujo vigente de recuperacion de contraseña queda documentado como codigo temporal de 6 digitos
- `User.serialize()` deja de exponer `password_hash`, `reset_code` y expiracion del codigo
- Mailjet, IMAP y SMTP/iCalendar quedan ubicados en `app/integrations/`
- los `print` de flujos sensibles fueron reemplazados por logging
- el mapa tecnico y la estrategia minima de pruebas quedaron documentados

## Riesgos residuales

- falta validacion manual de lectura de mails y envio de eventos `.ics` con proveedores reales configurados
- el envio de correo para recuperacion de contraseña sigue acoplado a Mailjet y QA ya confirmo que ese proveedor no esta disponible
- las integraciones externas se movieron sin cambiar comportamiento base, pero requieren prueba manual adicional con credenciales reales o dobles controlados
- el historial de migraciones fue ajustado para soportar recreacion desde cero, pero conviene seguir simplificandolo cuando exista una suite automatizada

## Validacion tecnica ejecutada

- se implemento el comando `flask --app run.py recreate-db --yes`
- el comando fue ejecutado con exito sobre la base local `legalito_db`
- el comando fue ejecutado con exito tambien en QA
- la recreacion completa reconstruyo schema, aplico migraciones y cargo datos base
- `alembic_version` quedo en `1b52f91b47e5`
- la tabla `statuses` quedo con `active`, `suspended` y `deleted`
- `terms_and_conditions` quedo seeded con `v1`

## Validacion manual ejecutada

- en dev se validaron `register`, `login` y `forgot-password`
- en QA se validaron `health`, `register` y `login`
- en QA `forgot-password` devolvio `502`, confirmando que ya no responde falso exito cuando falla el proveedor
- en QA se confirmo que Mailjet ya no esta disponible como proveedor de envio y debe reemplazarse

## Proximos pasos

Estos puntos ya no bloquean el cierre del ajuste arquitectonico, pero quedan como follow-ups operativos:

- validar manualmente lectura de mails y envio de eventos `.ics`
- reemplazar Mailjet como proveedor de envio para recuperacion de contraseña y correos salientes
- mantener el runbook de QA actualizado con el flujo operativo vigente

## Criterio de cierre efectivo

Se considera que este plan queda cerrado porque:

- el bootstrap ya es explicito y reproducible
- el app factory ya no modifica estado operativo
- existe ADR formal para el patron de capas
- los dominios principales ya fueron homologados en `api`, `service`, pruebas y specs
- la reconstruccion de base fue validada en local y QA

Lo pendiente restante pertenece a operacion o integraciones externas, no a la base estructural del backend.

## Notas

- este archivo es operativo y no normativo
- si durante la ejecucion aparece una decision transversal estable, abrir ADR especifico
- la estrategia minima de pruebas queda documentada en `spec/architecture/testing.md`
