# API-008 Update legacy no implementado

## Estado

Borrador

## Objetivo

Registrar el contrato actual del endpoint legacy que hoy no esta implementado.

## Endpoint

- metodo: `PUT`
- ruta: `/api/email-accounts`

## Autenticacion

- protegida con JWT

## Request

### Body

```json
{}
```

## Response esperada

### Estado actual

```json
{}
```

## Errores esperados

- `401`: no autenticado
- `501`: no implementado

## Notas tecnicas

- el blueprint hace `abort(501)`
- no debe usarse como contrato funcional; el endpoint vigente para update es `PUT /api/email-accounts/<id>`
