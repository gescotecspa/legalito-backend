# Versionado de API

## Estado actual

Los blueprints observados se publican bajo prefijo `/api` y no se detecta version explicita en la ruta.

## Regla inicial

- Si un cambio rompe contrato existente, debe documentarse primero.
- Antes de introducir versionado en URL o headers, registrar la decision en un ADR.
- Mientras no exista version explicita, asumir compatibilidad retroactiva como criterio por defecto.
