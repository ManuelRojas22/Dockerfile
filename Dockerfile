# syntax=docker/dockerfile:1
# Imagen del proyecto. Se construye desde la RAIZ del repositorio:
#   docker build -t dockerize:dev .

# ---------- Etapa 1: dependencias -------------------------------------------
FROM python:3.13-slim AS deps

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Herramientas de compilacion para mysqlclient (se descartan en la imagen final)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

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

# Solo las librerias de MySQL en tiempo de ejecucion
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1000 appuser

COPY --from=deps /venv /venv

WORKDIR /app
COPY --chown=appuser:appuser . /app
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh \
    && mkdir -p /app/backend/staticfiles /app/backend/media \
    && chown -R appuser:appuser /app/backend/staticfiles /app/backend/media

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8000/', timeout=4).status == 200 else sys.exit(1)"

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["web"]
