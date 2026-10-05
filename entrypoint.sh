#!/bin/sh
# Entry point del contenedor.
#
# Aplica migraciones, recopila los estaticos y arranca Gunicorn en el puerto
# que indique el entorno.
#
# Compatible con:
#   - docker-compose (PostgreSQL en el servicio "db")
#   - Render (PostgreSQL externo, alcanzado por DATABASE_URL)
#
# NO asume ningun hostname de base de datos: todo se deduce de las variables
# de entorno, por eso funciona igual en local y en produccion.
set -e

cd /app/backend

# Espera a que la base de datos acepte conexiones TCP.
#
# El host y el puerto se leen de DATABASE_URL (o de DB_HOST / DB_PORT). Si no
# hay ninguna configurada se asume SQLite y no hay nada que esperar.
# Se desactiva con DB_WAIT=0.
esperar_base_datos() {
  if [ "${DB_WAIT:-1}" = "0" ]; then
    echo "[entrypoint] espera de base de datos desactivada (DB_WAIT=0)."
    return 0
  fi

  python - <<'PY'
import os
import socket
import sys
import time
from urllib.parse import urlparse

url = os.environ.get("DATABASE_URL", "")
host = os.environ.get("DB_HOST", "")
port = os.environ.get("DB_PORT", "")

if url:
    # Render entrega_INTERNAL_DATABASE_URL sin puerto explicito.
    parsed = urlparse(url if "//" in url else f"//{url}")
    host = host or (parsed.hostname or "")
    port = port or (parsed.port or 0) or 0

if not host:
    print("[entrypoint] sin host de base de datos configurado: no se espera.")
    sys.exit(0)

# 5432 es el puerto de PostgreSQL, que es el motor que usa el proyecto.
port = int(port or 5432)
attempts = int(os.environ.get("DB_WAIT_ATTEMPTS", "40"))
delay = float(os.environ.get("DB_WAIT_DELAY", "2"))

print(f"[entrypoint] esperando a PostgreSQL en {host}:{port} ...")

for attempt in range(1, attempts + 1):
    try:
        with socket.create_connection((host, port), timeout=5):
            print(f"[entrypoint] PostgreSQL responde ({attempt}/{attempts}).")
            sys.exit(0)
    except OSError:
        if attempt == attempts:
            print(
                f"[entrypoint] ERROR: PostgreSQL en {host}:{port} no respondio "
                f"tras {attempts} intentos.",
                file=sys.stderr,
            )
            sys.exit(1)
        time.sleep(delay)
PY
}

case "${1:-web}" in
  web)
    esperar_base_datos

    echo "[entrypoint] aplicando migraciones ..."
    python manage.py migrate --noinput

    if [ "${DJANGO_CARGAR_DATOS:-0}" = "1" ]; then
      echo "[entrypoint] cargando datos iniciales (planes y equipo) ..."
      python manage.py cargar_datos
    fi

    echo "[entrypoint] recopilando archivos estaticos ..."
    python manage.py collectstatic --noinput

    # Render inyecta PORT; en docker-compose se deja 8000.
    bind="0.0.0.0:${PORT:-8000}"
    echo "[entrypoint] arrancando Gunicorn en ${bind} ..."

    if [ "${DJANGO_DEV_SERVER:-0}" = "1" ]; then
      # Solo para desarrollo interactivo (recarga automatica).
      echo "[entrypoint] DJANGO_DEV_SERVER=1: usando el servidor de desarrollo."
      exec python manage.py runserver "${bind}"
    fi

    exec gunicorn config.wsgi:application \
      --bind "${bind}" \
      --workers "${GUNICORN_WORKERS:-3}" \
      --timeout "${GUNICORN_TIMEOUT:-60}" \
      --access-logfile - \
      --error-logfile -
    ;;

  admin)
    shift
    exec python manage.py createsuperuser "$@"
    ;;

  sh)
    shift
    exec /bin/sh "$@"
    ;;

  *)
    exec "$@"
    ;;
esac
