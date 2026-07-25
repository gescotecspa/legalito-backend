# Dominio

## Resumen

Este backend expone una API Flask para Legalito, una plataforma pensada como CRM legal para apoyar la gestion de clientes, causas, agenda, documentos, comunicaciones y conocimiento juridico.

La vision de producto contempla experiencias cliente movil y web app. Por lo mismo, los contratos del backend deben tratarse como base compartida de plataforma, no como integracion exclusiva de una unica interfaz.

## Direccion futura de IA

Legalito incorporara progresivamente capacidades de inteligencia artificial como colaborador de trabajo juridico, especialmente para apoyo en jurisprudencia, analisis preliminar de casos, revision de antecedentes y asistencia en documentos.

Estas capacidades quedan por ahora como direccion de producto. Antes de implementarlas deben definirse specs, contratos API, reglas de confidencialidad, consentimiento informado, revision humana y auditoria.

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
- colaboracion futura con IA para jurisprudencia, analisis de casos y apoyo documental, pendiente de especificacion formal

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
