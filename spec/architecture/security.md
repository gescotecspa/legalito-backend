# Seguridad

## Lineamientos iniciales

- No exponer secretos en codigo ni en specs.
- Documentar variables de entorno requeridas por integraciones externas.
- Tratar auth, recuperacion de contraseña y manejo de archivos como zonas sensibles.
- Registrar expiracion, validez y uso esperado de tokens o codigos temporales.
- Documentar restricciones de acceso para endpoints autenticados y no autenticados.

## Recuperacion de contraseña

El flujo vigente usa un `reset code` temporal de 6 digitos enviado por correo transaccional.

El codigo expira a los 15 minutos, se invalida al cambiar correctamente la contraseña y no debe serializarse en respuestas de usuario.

La generacion, validacion y persistencia del codigo debe vivir en la capa de servicio de autenticacion. Los blueprints solo deben traducir request/respuesta HTTP.

## Temas a completar

- politica de rotacion de secretos
- estrategia de revocacion o expiracion de JWT
- reglas de rate limiting para login y recuperacion de contraseña
- tratamiento de datos personales e imagenes
