# System Map

## Objetivo

Ubicar rapidamente los modulos actuales del backend, sus blueprints principales, el punto de orquestacion esperado y las integraciones o modelos mas visibles.

## Estructura transversal vigente

- `app/api/` expone blueprints y recursos HTTP
- `app/services/` concentra logica de aplicacion y validaciones de dominio
- `app/models/` representa persistencia
- `app/integrations/` encapsula proveedores externos o protocolos
- `app/utils/` queda reservado para helpers tecnicos acotados

Este criterio queda formalizado en [ADR-001-separacion-de-capas-y-bootstrap-explicito.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/architecture/adr/ADR-001-separacion-de-capas-y-bootstrap-explicito.md).

## Modulos detectados

### Auth

- blueprints: `app/api/auth.py`
- servicios: `app/services/auth_service.py`, `app/services/user_service.py`
- modelos: `app/models/user.py`, `app/models/status.py`
- integraciones: JWT, Bcrypt, `app/integrations/email_delivery.py`
- contratos documentados: `spec/apis/auth/`, `spec/use-cases/auth/`

### Users

- blueprints: `app/api/users.py`
- servicios: `app/services/user_service.py`
- modelos: `app/models/user.py`
- integraciones: almacenamiento de imagenes via helper local
- contratos documentados: `spec/apis/users/`, `spec/use-cases/users/`

### Email Accounts y Mails

- blueprints: `app/api/email_accounts.py`, `app/api/mails.py`
- servicios: `app/services/email_account_service.py`, `app/services/mail_service.py`
- modelos: `app/models/email_account.py`
- integraciones: `app/integrations/imap_reader.py`, filtro de remitente, creacion de eventos desde correo
- contratos documentados: `spec/apis/email_accounts/`, `spec/apis/mails/`, `spec/use-cases/email_accounts/`

### Events

- blueprints: `app/api/events.py`
- servicios: `app/services/event_service.py`
- modelos: `app/models/event.py`
- integraciones: `app/integrations/smtp_calendar.py`, generacion de adjuntos `.ics`
- contratos documentados: `spec/apis/events/`, `spec/use-cases/events/`

### Cases

- blueprints: `app/api/cases.py`
- servicios: `app/services/case_service.py`
- modelos: `app/models/case.py`, `app/models/case_user.py`
- contratos documentados: `spec/apis/cases/`, `spec/use-cases/cases/`

### Folios

- blueprints: `app/api/folios.py`
- servicios: `app/services/folio_service.py`
- modelos: `app/models/folio.py`
- contratos documentados: `spec/apis/folios/`, `spec/use-cases/folios/`

### Notifications

- blueprints: `app/api/notifications.py`
- servicios: `app/services/notification_service.py`
- modelos: `app/models/notification.py`
- contratos documentados: `spec/apis/notifications/`, `spec/use-cases/notifications/`

### Parameters

- blueprints: `app/api/parameters.py`
- servicios: `app/services/parameter_service.py`
- modelos: `app/models/parameter.py`
- contratos documentados: `spec/apis/parameters/`, `spec/use-cases/parameters/`

### Roles

- blueprints: `app/api/roles.py`
- servicios: `app/services/rol_service.py`
- modelos: `app/models/rol.py`
- contratos documentados: `spec/apis/roles/`, `spec/use-cases/roles/`

### Assistants

- blueprints: `app/api/assistants.py`
- servicios: `app/services/assistant_service.py`
- modelos: `app/models/assistant.py`
- contratos documentados: `spec/apis/assistants/`, `spec/use-cases/assistants/`

### Courthouses

- blueprints: `app/api/courthouses.py`
- servicios: `app/services/courthouse_service.py`
- modelos: `app/models/courthouse.py`
- contratos documentados: `spec/apis/courthouses/`, `spec/use-cases/courthouses/`

### Terms and Conditions

- blueprints: `app/api/terms_and_conditions_api.py`
- servicios: `app/services/terms_and_conditions_service.py`
- modelos: `app/models/terms_and_conditions.py`
- contratos documentados: `spec/apis/terms_and_conditions/`, `spec/use-cases/terms_and_conditions/`

### Health

- blueprints: `app/api/health.py`
- objetivo tecnico: smoke check liviano de disponibilidad
- contratos documentados: `spec/apis/health/`

### Images

- blueprints: `app/api/image.py`
- helpers: `app/utils/image_handler.py`
- objetivo tecnico: servir uploads de usuario con control de path traversal
- contratos documentados: `spec/apis/image/`

## Integraciones transversales detectadas

- base de datos relacional via SQLAlchemy
- migraciones Alembic
- JWT para autenticacion
- selector de entrega de correo en `app/integrations/email_delivery.py`
- SMTP propio para correos transaccionales e invitaciones de calendario
- proveedor HTTP legado opcional en `app/integrations/mailjet_email.py`
- SMTP para invitaciones de calendario en `app/integrations/smtp_calendar.py`
- IMAP para lectura de correos en `app/integrations/imap_reader.py`

## Estado actual del mapa

- el patron `api -> service -> model/integration` ya fue aplicado en los dominios mas sensibles del backend
- la mayoria de dominios funcionales ya tiene carpeta propia en `spec/apis/` y `spec/use-cases/`
- los pendientes mas importantes ya no son de estructura base, sino de validacion manual de integraciones y cierre del reemplazo definitivo del proveedor `api`
- la recuperacion de contraseña ya fue validada en QA con SMTP propio; sigue pendiente extender y validar el resto de integraciones de correo

## Uso recomendado

- antes de crear una spec nueva, identificar el dominio en este mapa
- luego documentar el comportamiento en `use-cases/<dominio>/`
- y el contrato tecnico en `apis/<dominio>/`
