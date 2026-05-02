# API-001 Health check

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint liviano de verificacion de disponibilidad del backend.

## Endpoint

- metodo: `GET`
- ruta: `/api/health`

## Autenticacion

- publica

## Request

### Body

```json
{}
```

## Response esperada

### Exito

```json
{
  "status": "ok"
}
```

## Errores esperados

- no define errores funcionales propios; cualquier falla implica indisponibilidad del proceso o del proxy

## Notas tecnicas

- responde desde `app/api/health.py`
- hoy no exige JWT
- se usa como smoke check interno y publico en QA
- no tiene `use-case` asociado porque no expresa comportamiento de negocio
