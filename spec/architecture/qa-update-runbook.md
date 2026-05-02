# Runbook QA

Manual operativo para futuras actualizaciones del backend en el servidor de QA.

## Objetivo

Dejar un flujo simple y repetible para:

- ubicar el proyecto en el servidor
- sincronizar el código con `origin/main`
- preservar la configuración local
- recrear la base cuando QA no tenga datos
- validar que el backend quedó operativo

## Ruta esperada en QA

El proyecto actualmente vive en:

```bash
/var/www/legalito-backend
```

## Exposicion del backend en QA

Actualmente el backend queda expuesto en dos niveles:

- internamente por `gunicorn` en `127.0.0.1:8000`
- publicamente a traves de `nginx` bajo `https://api.legalito.cl`

Referencias utiles:

- health interno:

```bash
http://127.0.0.1:8000/api/health
```

- health publico:

```bash
https://api.legalito.cl/api/health
```

Esto permite distinguir entre:

- problema de aplicacion o `gunicorn`
- problema de proxy/reverse proxy o TLS

## Contexto de despliegue en QA

Actualmente QA debe considerarse desplegado con estas piezas:

- acceso shell al servidor
- backend en `/var/www/legalito-backend`
- repo Git dentro del mismo directorio
- entorno virtual local en `venv/`
- configuración principal en `/etc/legalito.env`
- servicio `systemd` en `/etc/systemd/system/legalito.service`
- migraciones dentro de `migrations/versions/`

Suposiciones operativas para futuras actualizaciones:

- el código fuente se actualiza desde `origin/main`
- `/etc/legalito.env` se mantiene en el servidor y debe preservarse antes de cambios de código
- si QA no tiene datos relevantes, el flujo preferido es:
  - respaldar `/etc/legalito.env`
  - alinear el repo con `origin/main`
  - recrear la base con `flask --app run.py recreate-db --yes`
- si QA en el futuro conserva datos, debe usarse un flujo no destructivo basado en `db upgrade`

## Cuándo usar este flujo

Usar este runbook cuando:

- QA no tiene datos relevantes y se puede recrear completo
- queremos alinear el servidor con el estado real de `main`
- hay dudas sobre cambios locales viejos en el deploy

No usar `recreate-db` sin confirmar antes si QA tiene datos que deban conservarse.

## Prerrequisitos

- acceso shell al servidor
- acceso al repo Git remoto
- `venv` ya creado dentro del proyecto
- archivo `/etc/legalito.env` presente y completo

Variables mínimas a revisar:

- `DATABASE_URL`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `MAILJET_API_KEY`
- `MAILJET_API_SECRET`
- `MAILJET_SENDER_EMAIL`
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `ALLOWED_SENDER`

Referencia de servicio actual:

```ini
[Service]
WorkingDirectory=/var/www/legalito-backend
EnvironmentFile=/etc/legalito.env
ExecStart=/var/www/legalito-backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"
```

Referencia operativa de exposicion:

- `systemd`: `legalito.service`
- backend interno: `127.0.0.1:8000`
- dominio publico esperado: `https://api.legalito.cl`

## Flujo recomendado

### 1. Entrar al proyecto

```bash
cd /var/www/legalito-backend
```

### 2. Revisar estado actual

```bash
git rev-parse --short HEAD
git status --short
git branch --show-current
```

Si el árbol está sucio y QA no tiene datos, conviene resetear el código al remoto en vez de intentar mezclar cambios locales viejos.

### 3. Respaldar configuración del servidor

```bash
cp /etc/legalito.env /root/legalito.env.qa.bak
```

Si el servidor usa otro usuario o política de backups, ajustar la ruta de respaldo.

### 4. Traer remoto y validar el commit objetivo

```bash
git fetch origin
git log --oneline origin/main -5
```

Confirmar que el commit esperado aparezca en `origin/main`.

### 5. Alinear el deploy con `origin/main`

Solo cuando QA pueda recrearse sin riesgo:

```bash
git reset --hard origin/main
```

Verificación:

```bash
git rev-parse --short HEAD
git status --short
```

El resultado esperado es:

- HEAD alineado al commit remoto deseado
- working tree limpio

### 6. Activar entorno virtual

```bash
source venv/bin/activate
```

### 7. Cargar variables del servidor en la shell actual

Para ejecutar `flask --app run.py ...` manualmente desde terminal, hay que exportar también las variables de `/etc/legalito.env`.

```bash
set -a
source /etc/legalito.env
set +a
```

Verificación rápida:

```bash
echo "$DATABASE_URL"
echo "$SECRET_KEY"
echo "$JWT_SECRET_KEY"
```

### 8. Revisar configuración crítica

```bash
grep -E "^(DATABASE_URL|SECRET_KEY|JWT_SECRET_KEY|MAILJET_|SMTP_|ALLOWED_SENDER)" /etc/legalito.env
```

Si falta `SECRET_KEY` o `DATABASE_URL`, el backend no debería arrancar correctamente.

### 9. Recrear base y seed inicial

```bash
flask --app run.py recreate-db --yes
```

Este comando:

- recrea el schema `public`
- corre migraciones
- ejecuta `setup-initial-data`

## Validaciones posteriores

### 10. Confirmar seed base

```bash
psql "$DATABASE_URL" -c "SELECT id, code, label FROM statuses ORDER BY id;"
psql "$DATABASE_URL" -c "SELECT id, version FROM terms_and_conditions ORDER BY id;"
```

Resultado esperado:

- `statuses` contiene `active`, `suspended` y `deleted`
- `terms_and_conditions` contiene al menos `v1`

### 11. Confirmar rutas/CLI

```bash
flask --app run.py routes
```

### 12. Reiniciar servicio y smoke test mínimo

```bash
systemctl restart legalito
systemctl status legalito --no-pager
```

Validar manualmente:

- `health`
- `register`
- `login`
- `forgot-password`
- `reset-password`
- lectura de mails
- envío de eventos `.ics`

Checks recomendados:

```bash
curl -i http://127.0.0.1:8000/api/health
curl -i https://api.legalito.cl/api/health
```

## Troubleshooting rápido

### Hay cambios locales inesperados

Revisar:

```bash
git status --short
git diff -- app/__init__.py config.py
git diff -- migrations/versions
```

Si QA no tiene datos y el deploy está desalineado, usar:

```bash
git fetch origin
git reset --hard origin/main
```

### Falta la variable de base de datos

El proyecto usa `DATABASE_URL`, no `DATABASE_URI`.

### `source /etc/legalito.env` falla o deja `DATABASE_URL` vacía

Si la contraseña de la URL contiene caracteres especiales como `&`, dejar el valor entre comillas simples:

```env
DATABASE_URL='postgresql://usuario:clave&especial@localhost:5432/base?sslmode=disable'
```

Lo mismo aplica a `SECRET_KEY` y `JWT_SECRET_KEY` si se quiere mantener formato seguro para shell.

### La app no arranca por clave secreta

Verificar:

- `SECRET_KEY`
- `JWT_SECRET_KEY`

El backend ya no usa fallback inseguro para `SECRET_KEY`.

### El bootstrap falla con migraciones

Validar primero que el repo realmente quedó en el commit esperado y sin cambios locales.

## Notas operativas

- Si QA va a conservar datos en el futuro, este runbook debe complementarse con un flujo no destructivo basado en `flask --app run.py db upgrade`.
- Para ambientes vacíos o descartables, el flujo preferido es `git reset --hard origin/main` + `flask --app run.py recreate-db --yes`.
- Para comandos manuales de Flask en QA no basta con activar `venv`; también hay que exportar `/etc/legalito.env` en la shell actual.
