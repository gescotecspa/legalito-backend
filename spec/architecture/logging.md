# Logging

## Criterio inicial

- Loggear eventos tecnicos relevantes sin exponer secretos ni datos sensibles.
- Priorizar trazabilidad en auth, lectura de correos, envio de mails y operaciones de integracion.
- Evitar `print` en codigo productivo cuando corresponda usar logging estructurado o al menos `app.logger`.

## Pendientes

- definir formato comun de logs
- definir niveles esperados por tipo de evento
- definir correlacion entre request, errores e integraciones externas
