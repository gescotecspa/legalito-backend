# API-001 Servir imagen de usuario

## Estado

Borrador

## Objetivo

Describir el contrato tecnico del endpoint que entrega archivos desde el directorio permitido de uploads de usuario.

## Endpoint

- metodo: `GET`
- ruta: `/api/static/uploads/users/<filename>`

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
{}
```

Respuesta binaria con `mimetype` inferido a partir del nombre del archivo.

## Errores esperados

- `404`: archivo inexistente o intento de path traversal
- `500`: error inesperado al leer el archivo

## Notas tecnicas

- resuelve rutas bajo `static/uploads/users`
- bloquea path traversal validando que la ruta resuelta permanezca dentro del directorio permitido
- el contenido exitoso se devuelve como binario, no como JSON
- no tiene `use-case` asociado porque no expresa comportamiento de negocio
