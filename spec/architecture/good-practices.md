# Buenas Practicas

- Mantener la logica de negocio fuera de los blueprints.
- Evitar mezclar plantillas, contratos HTTP y acceso a datos en un mismo archivo.
- Reutilizar servicios para integraciones externas y flujos transaccionales.
- Documentar primero cambios de comportamiento o contrato antes de cambios grandes.
- Agregar pruebas o validaciones manuales trazables cuando se modifique auth, correo o persistencia.
- No introducir nuevas integraciones externas sin dejar su configuracion y riesgo documentados.
