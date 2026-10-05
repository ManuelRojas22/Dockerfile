# syntax=docker/dockerfile:1
# Imagen del proyecto. Se construye desde la RAIZ del repositorio:
#   docker build -t dockerize:dev .

# ---------- Etapa 1: dependencias -------------------------------------------
FROM python:3.13-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# psycopg[binary] y dj-database-url traen ruedas ya compiladas, asi que no hace
# falta ningun compilador ni cliente de MySQL en la imagen.
COPY backend/requirements.txt ./requirements.txt
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install -r requirements.txt

# ---------- Etapa 2: imagen de ejecucion ------------------------------------
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/venv/bin:$PATH"

RUN useradd --create-home --uid 1000 appuser

COPY --from=deps /venv /venv

WORKDIR /app
COPY --chown=appuser:appuser . /app
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh \
    && mkdir -p /app/backend/staticfiles /app/backend/media \
    && chown -R appuser:appuser /app/backend/staticfiles /app/backend/media

USER appuser

EXPOSE 8000

# El puerto lo fija el entorno: Render inyecta PORT (por defecto 10000) y
# docker-compose deja 8000. El healthcheck debe consultar el mismo puerto que
# escucha Gunicorn, por eso se lee de $PORT y no se escribe 8000 a mano.
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD python -c "import os,sys,urllib.request; port=os.environ.get('PORT','8000'); sys.exit(0 if urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=4).status==200 else sys.exit(1))"

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["web"]
