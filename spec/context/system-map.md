# System Map

## Objetivo

Ubicar rapidamente los modulos actuales del backend, sus blueprints principales y las integraciones o modelos mas visibles.

## Modulos detectados

### Auth

- blueprints: `app/api/auth.py`
- servicios: `app/services/auth_service.py`, `app/services/user_service.py`
- modelos: `app/models/user.py`, `app/models/status.py`
- integraciones: JWT, Bcrypt, `app/integrations/mailjet_email.py`

### Users

- blueprints: `app/api/users.py`
- servicios: `app/services/user_service.py`
- modelos: `app/models/user.py`
- integraciones: almacenamiento de imagenes via helper local

### Email Accounts y Mails

- blueprints: `app/api/email_accounts.py`, `app/api/mails.py`
- servicios: `app/services/email_account_service.py`
- modelos: `app/models/email_account.py`
- integraciones: `app/integrations/imap_reader.py`, filtro de remitente, creacion de eventos desde correo

### Events

- blueprints: `app/api/events.py`
- servicios: `app/services/event_service.py`
- modelos: `app/models/event.py`
- integraciones: `app/integrations/smtp_calendar.py`, generacion de adjuntos `.ics`

### Cases

- blueprints: `app/api/cases.py`
- servicios: `app/services/case_service.py`
- modelos: `app/models/case.py`, `app/models/case_user.py`

### Folios

- blueprints: `app/api/folios.py`
- servicios: `app/services/folio_service.py`
- modelos: `app/models/folio.py`

### Notifications

- blueprints: `app/api/notifications.py`
- servicios: `app/services/notification_service.py`
- modelos: `app/models/notification.py`

### Parameters

- blueprints: `app/api/parameters.py`
- servicios: `app/services/parameter_service.py`
- modelos: `app/models/parameter.py`

### Roles

- blueprints: `app/api/roles.py`
- servicios: `app/services/rol_service.py`
- modelos: `app/models/rol.py`

### Assistants

- blueprints: `app/api/assistants.py`
- servicios: `app/services/assistant_service.py`
- modelos: `app/models/assistant.py`

### Courthouses

- blueprints: `app/api/courthouses.py`
- servicios: `app/services/courthouse_service.py`
- modelos: `app/models/courthouse.py`

### Terms and Conditions

- blueprints: `app/api/terms_and_conditions_api.py`
- servicios: `app/services/terms_and_conditions_service.py`
- modelos: `app/models/terms_and_conditions.py`

### Images

- blueprints: `app/api/image.py`
- helpers: `app/utils/image_handler.py`

## Integraciones transversales detectadas

- base de datos relacional via SQLAlchemy
- migraciones Alembic
- JWT para autenticacion
- Mailjet para mails transaccionales en `app/integrations/mailjet_email.py`
- SMTP para invitaciones de calendario en `app/integrations/smtp_calendar.py`
- IMAP para lectura de correos en `app/integrations/imap_reader.py`

## Uso recomendado

- antes de crear una spec nueva, identificar el dominio en este mapa
- luego documentar el comportamiento en `use-cases/<dominio>/`
- y el contrato tecnico en `apis/<dominio>/`
