# Integraciones

## Integraciones detectadas

- SMTP propio para correo transaccional de recuperacion de contraseña
- SMTP para envio de invitaciones de calendario con `.ics`
- IMAP para lectura de correos externos asociados a usuarios

## Ubicacion esperada

Las integraciones externas deben vivir en `app/integrations/`.

- selector de entrega: `app/integrations/email_delivery.py`
- SMTP reset email: `app/integrations/local_smtp_email.py`
- proveedor HTTP legado: `app/integrations/mailjet_email.py`
- SMTP/iCalendar: `app/integrations/smtp_calendar.py`
- IMAP: `app/integrations/imap_reader.py`

Los blueprints y servicios pueden orquestar casos de uso, pero no deberian contener detalles de protocolo, autenticacion con proveedores externos ni armado de payloads propios de cada integracion.

## Regla de documentacion

Cada integracion nueva o modificada deberia dejar documentado:

- objetivo de negocio
- proveedor usado
- variables de entorno requeridas
- manejo de errores
- impacto en seguridad
- estrategia de prueba o validacion manual

## Estrategia de entrega de correo

La seleccion del mecanismo de envio de correo debe resolverse por configuracion y no por ramas de negocio en los servicios.

Referencia de diseno:

- [email-delivery-strategy.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/architecture/email-delivery-strategy.md)

Resumen:

- parametro unico inicial: `EMAIL_DELIVERY_METHOD`
- valores esperados: `local` o `api`
- `local` usa SMTP autenticado y es la opcion por defecto
- `api` usa proveedor HTTP externo
