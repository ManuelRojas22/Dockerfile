#!/bin/sh
# Entry point del contenedor.
# Espera a MySQL, aplica migraciones y arranca el servicio pedido.
set -e

cd /app/backend

esperar_mysql() {
  host="${MYSQL_HOST:-db}"
  port="${MYSQL_PORT:-3306}"
  intentos="${DB_WAIT_ATTEMPTS:-40}"

  echo "[entrypoint] esperando MySQL en ${host}:${port} ..."
  i=1
  while [ "$i" -le "$intentos" ]; do
    if python -c "
import socket, sys
s = socket.socket()
s.settimeout(3)
try:
    s.connect(('${host}', ${port}))
except OSError:
    sys.exit(1)
finally:
    s.close()
" 2>/dev/null; then
      echo "[entrypoint] MySQL responde. Continuando."
      return 0
    fi
    i=$((i + 1))
    sleep 2
  done

  echo "[entrypoint] ERROR: MySQL no respondio tras ${intentos} intentos." >&2
  return 1
}

case "${1:-web}" in
  web)
    # Solo el servicio web necesita MySQL disponible antes de arrancar.
    esperar_mysql

    echo "[entrypoint] aplicando migraciones ..."
    python manage.py migrate --noinput

    if [ "${DJANGO_CARGAR_DATOS:-0}" = "1" ]; then
      echo "[entrypoint] cargando datos iniciales (planes y equipo) ..."
      python manage.py cargar_datos
    fi

    if [ "${DJANGO_DEBUG:-False}" = "False" ]; then
      echo "[entrypoint] recopilando archivos estaticos ..."
      python manage.py collectstatic --noinput
    fi

    if [ "${DJANGO_DEBUG:-False}" = "False" ]; then
      echo "[entrypoint] arrancando Gunicorn ..."
      exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers "${GUNICORN_WORKERS:-3}" \
        --timeout "${GUNICORN_TIMEOUT:-60}" \
        --access-logfile - \
        --error-logfile -
    fi

    echo "[entrypoint] arrancando servidor de desarrollo ..."
    exec python manage.py runserver 0.0.0.0:8000
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
