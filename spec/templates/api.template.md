# API-XXX Nombre del endpoint

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint.

## Endpoint

- metodo: `POST`
- ruta: `/api/...`

## Autenticacion

- publica o protegida

## Request

### Body

```json
{}
```

## Response esperada

### Exito

```json
{}
```

## Diagrama Mermaid opcional

Usar solo si el endpoint orquesta servicios, persistencia o integraciones externas.

```mermaid
sequenceDiagram
  participant Client
  participant API
  participant Service
  Client->>API: Request
  API->>Service: Ejecuta caso
  Service-->>API: Resultado
  API-->>Client: Response
```

## Errores esperados

- `400`: validacion
- `401`: no autenticado
- `403`: no autorizado
- `404`: no encontrado

## Notas tecnicas

- dependencia externa
- persistencia afectada
