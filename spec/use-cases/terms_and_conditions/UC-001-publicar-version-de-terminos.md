# UC-001 Publicar version de terminos

## Estado

Borrador

## Objetivo

Permitir registrar una nueva version de terminos y condiciones.

## Actores

- cliente consumidor de API
- backend de terminos y condiciones

## Disparador

Se requiere publicar una nueva version legal.

## Precondiciones

- se informa `content` y `version`
- la version no existe previamente

## Flujo principal

1. El cliente envia contenido y version.
2. El backend valida campos requeridos.
3. El backend verifica unicidad de la version.
4. El backend persiste la nueva version.
5. El backend responde el recurso creado.

## Flujos alternativos

- Si faltan campos requeridos, el flujo se rechaza.
- Si la version ya existe, el flujo se rechaza.

## Reglas de negocio

- una version no puede repetirse

## Postcondiciones

- queda disponible una nueva version de terminos

## Criterios de aceptacion

- dado contenido y version unicos, cuando se crea la nueva version, entonces queda persistida y disponible como recurso
