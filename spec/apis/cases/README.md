# APIs Cases

Specs de contratos HTTP relacionados con creacion, listado y gestion de causas.

## Specs disponibles

- [API-001-cases-create.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/apis/cases/API-001-cases-create.md)
- [API-002-cases-byuser.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/apis/cases/API-002-cases-byuser.md)
- [API-003-cases-delete.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/apis/cases/API-003-cases-delete.md)
- [API-004-cases-get-by-id.md](/Users/marcosceliz/Projects/Gescotec/legalito/legalito-backend/spec/apis/cases/API-004-cases-get-by-id.md)

## Estado del dominio

- dominio ya corregido para usar identidad JWT en `cases/byUser`
- `GET /cases/<id>` ya valida ownership por JWT y serializa cliente asociado cuando existe
- cobertura automatizada basica agregada para servicio y API
- faltan specs y pruebas para `GET /cases/list`
- `PUT /cases` sigue no implementado
