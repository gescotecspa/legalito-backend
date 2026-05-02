# UC-001 Registrar cuenta de correo

## Estado

Borrador

## Objetivo

Permitir al usuario autenticado registrar una cuenta de correo para integraciones IMAP.

## Actores

- usuario autenticado
- backend de cuentas de correo

## Disparador

El usuario desea conectar una casilla para lectura automatica.

## Precondiciones

- el usuario esta autenticado
- el usuario existe en la base
- la direccion de correo no esta ya registrada

## Flujo principal

1. El usuario envia proveedor, servidor IMAP, email y password.
2. El backend inyecta el usuario autenticado.
3. El backend valida existencia del usuario y unicidad del correo.
4. El backend persiste la cuenta activa.
5. El backend responde la cuenta creada.

## Flujos alternativos

- Si el usuario no existe o el correo ya esta en uso, el flujo se rechaza.

## Reglas de negocio

- `email_address` debe ser unico en la tabla
- la cuenta se crea activa por defecto

## Postcondiciones

- la cuenta de correo queda asociada al usuario autenticado

## Criterios de aceptacion

- dado un usuario autenticado con datos validos, cuando registra una cuenta, entonces la cuenta queda persistida y asociada a ese usuario
