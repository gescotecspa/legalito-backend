# API-001 Listar roles

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que retorna el catalogo de roles.

## Endpoint

- metodo: `GET`
- ruta: `/api/roles`

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
[
  {
    "id": 1,
    "name": "Admin",
    "description": "Administrador"
  }
]
```

## Errores esperados

- `500`: error inesperado de lectura

## Notas tecnicas

- delega a `app.services.rol_service.list_roles_service`
- serializa el modelo `Rol` sin transformaciones adicionales
- tiene coverage automatizada basica del servicio y del endpoint
