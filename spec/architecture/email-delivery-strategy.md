# Estrategia de entrega de correo

## Estado

Implementacion inicial en uso para recuperacion de contrasena

## Objetivo

Definir una estrategia simple y consistente para que el backend pueda enviar correos usando un metodo configurable por entorno, evitando acoplar los servicios de negocio a un proveedor especifico.

## Decision de diseno

Se adopta un unico parametro de configuracion para seleccionar el mecanismo de entrega de correo:

```env
EMAIL_DELIVERY_METHOD=local
```

`local` pasa a ser el valor preferido y por defecto para nuevos entornos.

Valores validos iniciales:

- `local`
- `api`

## Semantica de cada valor

### `local`

- usa SMTP autenticado configurado en el entorno
- pensado para entornos donde existe relay SMTP utilizable o para desarrollo controlado
- implementado para recuperacion de contraseña
- soporta `STARTTLS` por defecto y `SSL` directo por configuracion cuando el servidor SMTP lo requiera

### `api`

- usa un proveedor externo por HTTP API
- pensado para QA o produccion cuando el VPS o la red no permiten envio SMTP saliente confiable
- hoy mantiene compatibilidad con la integracion existente de Mailjet

## Alcance inicial

El parametro debe gobernar el envio de:

- recuperacion de contraseña
- correos salientes transaccionales del sistema

En una primera etapa no se separa por tipo de correo. El sistema usa una sola estrategia global de entrega.

## Criterio de arquitectura

- los servicios de negocio no deben conocer el proveedor concreto
- `auth_service` y demas servicios deben invocar una capa de envio abstracta
- la seleccion de `local` o `api` debe resolverse por configuracion
- los detalles de SMTP o del proveedor HTTP deben vivir en `app/integrations/`

## Variables de entorno esperadas

### Comunes

```env
EMAIL_DELIVERY_METHOD=local
```

### Si `EMAIL_DELIVERY_METHOD=local`

```env
SMTP_SERVER=...
SMTP_PORT=587
SMTP_USERNAME=...
SMTP_PASSWORD=...
SMTP_DEFAULT_SENDER=...
SMTP_USE_TLS=true
SMTP_USE_SSL=false
```

### Si `EMAIL_DELIVERY_METHOD=api`

Las credenciales exactas dependen del proveedor implementado. Mientras exista Mailjet, el backend espera:

```env
MAILJET_API_KEY=...
MAILJET_API_SECRET=...
MAILJET_SENDER_EMAIL=...
```

## Comportamiento esperado ante configuracion incompleta

- si el metodo configurado es `local` y faltan credenciales SMTP, el backend debe fallar de forma explicita al intentar enviar
- si el metodo configurado es `api` y faltan credenciales del proveedor, el backend debe fallar de forma explicita al intentar enviar
- el error hacia la capa de aplicacion debe ser uniforme, independientemente del proveedor real

## No objetivos por ahora

- fallback automatico entre `api` y `local`
- estrategia distinta por tipo de correo
- cola de reintentos
- multiplexar varios proveedores al mismo tiempo

## Riesgos y motivacion

- algunos VPS o proveedores de hosting bloquean o limitan el envio SMTP saliente
- depender de un solo proveedor externo sin abstraccion vuelve costoso un reemplazo
- mezclar decision de proveedor dentro de `auth_service` o `event_service` aumentaria el acoplamiento

## Siguiente paso esperado

- extender la misma abstraccion a mas correos salientes cuando corresponda
- reemplazar Mailjet por el proveedor API definitivo cuando quede decidido
- mantener `smtp_calendar.py` e integraciones futuras alineadas al mismo criterio cuando corresponda
