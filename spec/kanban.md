# Kanban Operativo

Tablero simple para seguir trabajo activo del backend sin depender de notas externas.

## Como usarlo

- mover cada tarea entre secciones segun su estado
- mantener tareas chicas y concretas
- cuando una tarea cambie comportamiento o contrato, reflejarlo tambien en `spec/use-cases/` o `spec/apis/`
- usar `Notas` para bloqueos, decisiones o proximos checks

## Todo

- publicar en QA o entorno correspondiente los ultimos cambios ya subidos al repo
- agregar/ajustar variables de entorno requeridas para habilitar SMTP propio antes del proximo deploy
- validar manualmente lectura de mails y envio de eventos `.ics`
- validar manualmente recuperacion de contraseña usando SMTP propio
- dejar el reemplazo del proveedor `api` actual de correo saliente (hoy Mailjet) como segundo frente separado

## En curso

- sin tareas activas en este momento

## Hecho

- estabilizar bootstrap y setup operativo
- sacar side effects del arranque HTTP
- mover setup inicial a comando Flask explicito
- documentar flujo de arranque esperado
- documentar flujos operativos para base nueva, recreacion total y actualizacion incremental
- implementar comando `flask --app run.py recreate-db --yes`
- validar tecnicamente recreacion completa de base local con migraciones y seed inicial
- validar recreacion completa y seed inicial en QA
- agregar pruebas automatizadas para `auth_service` y `app/api/auth.py`
- validar manualmente flujo base de `auth` en dev
- validar manualmente flujo base de `auth` en QA
- agregar seed/bootstrap minimo de `terms_and_conditions` para entornos limpios
- hacer que `forgot-password` no responda exito cuando Mailjet falla
- separar validacion HTTP de logica de aplicacion en endpoints de prioridad alta:
- `app/api/mails.py:read_mails`
- `app/api/events.py:create_and_send_event`
- `app/api/notifications.py:list_notifications_by_user`
- separar validacion HTTP de logica de aplicacion en endpoints de prioridad media:
- `app/api/events.py:list_events_by_user`
- `app/api/events.py:edit_event`
- `app/api/email_accounts.py:update_account`
- `app/api/terms_and_conditions_api.py:AcceptTermsResource.put`
- definir criterio de arquitectura estable mediante ADR:
- `ADR-001-separacion-de-capas-y-bootstrap-explicito`
- agregar pruebas basicas para app factory y bootstrap
- exigir JWT obligatorio en endpoints sensibles que hoy aceptaban identidad por body o ruta:
- `app/api/mails.py:read_mails`
- `app/api/notifications.py:list_notifications_by_user`
- `app/api/terms_and_conditions_api.py:AcceptTermsResource.put`
- dejar de exponer `password` en serializacion de `EmailAccount`
- eliminar fallback inseguro de `SECRET_KEY` y exigir configuracion explicita al arrancar
- blindar `app/api/image.py` contra path traversal
- reforzar ownership checks en endpoints por `id` de notifications y email accounts
- definir e implementar estrategia minima de rate limiting para login y recuperacion de contraseña
- refactorizar vertical `auth` a patron `api -> service -> model/integration`
- mover `delete-account` al dominio `users` y agregar pruebas basicas
- homologar dominio `cases`:
- separar validacion HTTP de logica de aplicacion
- corregir uso de identidad en `cases/byUser`
- crear specs `API-XXX` y `UC-XXX`
- agregar pruebas automatizadas basicas
- homologar dominio `assistants`:
- documentar contratos principales
- agregar pruebas de favoritos, filtro y profile
- revisar ownership y consistencia de respuestas
- homologar dominio `folios`:
- documentar contratos actuales
- agregar pruebas API basicas de create/list/delete
- homologar dominios de catalogo `parameters`, `roles` y `courthouses`:
- crear specs minimas por endpoint
- agregar pruebas API basicas de lectura
- validar si requieren autenticacion consistente
- completar specs pendientes de dominios ya expuestos en `app/api/`:
- `notifications`
- `email_accounts`
- `terms_and_conditions`
- definir tratamiento documental minimo para `health` e `image`
- actualizar mapa tecnico del sistema
- cerrar plan de ajuste con resumen y riesgos residuales
- mover Mailjet, IMAP y SMTP/iCalendar a `app/integrations/`
- definir estrategia minima de pruebas para refactors de arquitectura
- definir estrategia simple de entrega de correo por parametro global
- implementar seleccion de entrega de correo por `EMAIL_DELIVERY_METHOD` con soporte `local|api`

## Notas

- fuente principal del ajuste actual: `spec/architecture/architecture-setup.tasks.md`
- este tablero no reemplaza specs; solo ayuda a recordar y priorizar
- estado de referencia actual:
- `flask --app run.py recreate-db --yes` ejecutado con exito sobre `legalito_db`
- Alembic queda en revision `1b52f91b47e5`
- `statuses` queda seeded con `active`, `suspended` y `deleted`
- `terms_and_conditions` queda seeded con version minima `v1`
- pruebas automatizadas totales actuales: 108 tests verdes con `python -m unittest discover -s tests -p 'test_*.py' -v`
- controles de seguridad ya aplicados:
- JWT obligatorio en endpoints sensibles
- `EmailAccount` ya no expone `password`
- `SECRET_KEY` obligatoria al arrancar
- proteccion contra path traversal en imagenes
- ownership checks reforzados por `id`
- rate limiting minimo en `login`, `forgot-password` y `reset-password`
- validacion manual `auth` en dev:
- sobre base limpia recreada, `register` funciona sin inserciones manuales de terminos
- `forgot-password` devuelve `502` cuando Mailjet responde no exitoso
- validacion manual `auth` en QA:
- `health` responde `200`
- `register` responde `201`
- `login` responde `200`
- `forgot-password` responde `502`
- `forgot-password` falla porque Mailjet ya no esta disponible como proveedor de envio en QA
- pendientes de homologacion mas visibles hoy:
- `mails/events` siguen pendientes de validacion manual real
- vacios documentales visibles hoy:
- existen specs para `auth`, `users`, `cases`, `assistants`, `folios`, `parameters`, `roles`, `courthouses`, `events`, `mails`, `notifications`, `email_accounts` y `terms_and_conditions`
- `health` e `image` quedaron documentados solo a nivel `API` por ser endpoints tecnicos sin `use-case` de negocio
- estado de integraciones externas:
- `app/integrations/mailjet_email.py` se usa desde `auth_service`
- `app/integrations/imap_reader.py` y `app/integrations/smtp_calendar.py` se usan desde `mail_service` y `event_service`
- estrategia minima de pruebas para refactors:
- queda formalizada en `spec/architecture/testing.md`
- se considera criterio persistente del repo para futuras sesiones y cambios
- estrategia de entrega de correo:
- queda documentada en `spec/architecture/email-delivery-strategy.md`
- se adopta un unico parametro inicial `EMAIL_DELIVERY_METHOD` con valores `local` o `api`
- estado actual de implementacion:
- `EMAIL_DELIVERY_METHOD=local` ya soporta recuperacion de contraseña via SMTP autenticado
- `EMAIL_DELIVERY_METHOD=api` mantiene compatibilidad con la integracion actual basada en Mailjet
