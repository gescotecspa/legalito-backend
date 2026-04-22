# Persistencia

## Base actual

- SQLAlchemy como ORM principal
- Alembic para migraciones
- modelos ubicados en `app/models/`

## Reglas iniciales

- Todo cambio persistente debe ir acompañado de migracion cuando corresponda.
- Campos nuevos con impacto funcional deben quedar reflejados en specs de negocio o API.
- Evitar que validaciones criticas existan solo en la capa HTTP.

## Pendientes

- documentar relaciones principales del dominio
- definir criterio de borrado logico vs borrado fisico por entidad
- definir politicas de integridad y unicidad relevantes
