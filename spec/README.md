# Spec del Backend

Este directorio concentra la especificacion funcional y tecnica del backend de Legalito.

## Objetivo

Evitar que decisiones, contratos y tareas queden dispersos entre codigo, chats y notas temporales.

## Estructura

- `context/`: lenguaje comun y panorama del dominio.
- `architecture/`: lineamientos tecnicos y decisiones transversales.
- `architecture/adr/`: decisiones arquitectonicas que deben mantenerse estables.
- `use-cases/`: comportamiento de negocio esperado, agrupado por dominio.
- `apis/`: contratos tecnicos de endpoints y errores, agrupados por dominio.
- `templates/`: plantillas para crear nuevos artefactos.

## Como usar esta carpeta

1. Si cambia comportamiento de negocio, crear o ajustar un archivo dentro del dominio correspondiente en `use-cases/`.
2. Si cambia un endpoint o contrato tecnico, crear o ajustar un archivo dentro del dominio correspondiente en `apis/`.
3. Si aparece una decision transversal, registrar un ADR en `architecture/adr/`.
4. Si hace falta seguimiento operativo, crear un archivo `*.tasks.md` junto al artefacto principal.

## Agrupacion por dominio

La carpeta debe crecer por dominios funcionales del backend, por ejemplo:

- `use-cases/auth/`
- `use-cases/users/`
- `use-cases/events/`
- `apis/auth/`
- `apis/users/`
- `apis/mails/`

## Convencion de nombres

- use cases: `UC-XXX-nombre-corto.md`
- apis: `API-XXX-recurso-o-endpoint.md`
- adrs: `ADR-XXX-titulo-corto.md`
- tasks asociadas: mismo nombre base con sufijo `.tasks.md`

Ejemplos:

- `use-cases/auth/UC-001-registro-de-usuario.md`
- `apis/auth/API-001-auth-register.md`
- `apis/auth/API-001-auth-register.tasks.md`

## Regla de separacion

- `use-cases/` define que debe pasar.
- `apis/` define como se expone tecnicamente.
- `adr/` define decisiones tecnicas transversales.
- `tasks` solo registra avance, dependencias y validaciones pendientes.

## Diagramas Mermaid

Mermaid puede usarse como apoyo visual en specs cuando aclare un flujo, estado, dependencia o decision.

Uso esperado:

- `use-cases/`: flujos de negocio, caminos alternativos o estados funcionales.
- `apis/`: secuencia request/response, orquestacion de servicios o integraciones externas.
- `architecture/`: capas, dependencias, integraciones, bootstrap o decisiones tecnicas.
- `architecture/adr/`: contexto visual de la decision o alternativas relevantes.

No usar Mermaid en archivos `*.tasks.md`; esos archivos son seguimiento operativo y deben mantenerse como checklist/resumen.

El diagrama complementa el texto, no lo reemplaza. Si el diagrama repite una lista simple, no hace falta incluirlo.

## Convenciones

- Escribir en espanol.
- Preferir cambios pequenos y trazables.
- Evitar duplicar reglas entre `use-cases/` y `apis/`.
- Si una decision tecnica afecta varias areas, documentarla como ADR antes de propagarla.
- Mantener el inventario tecnico del sistema en `context/system-map.md`.
