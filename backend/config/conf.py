"""Configuracion del proyecto resuelta desde el entorno, en POO.

Este modulo centraliza toda la configuracion "dura" del proyecto en clases.
`settings.py` solo se limita a exponer estos valores con los nombres que
Django espera a nivel de modulo.
"""

import os
from pathlib import Path
from urllib.parse import quote

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Raiz del proyecto: .../proyecto basico
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Raiz del backend: .../proyecto basico/backend
BACKEND_DIR = BASE_DIR / "backend"

# Raiz del frontend: .../proyecto basico/frontend
FRONTEND_DIR = BASE_DIR / "frontend"

# Clave que se usa SOLO cuando nadie define DJANGO_SECRET_KEY. Es publica y
# conocida: con DEBUG=False el proyecto no debe arrancar nunca con ella.
DEV_SECRET_KEY = "django-insecure-clave-de-desarrollo-cambiar-en-produccion"


class Environment:
    """Lector tipado de variables de entorno (soporta archivo .env)."""

    ENV_FILE = BACKEND_DIR / ".env"

    @classmethod
    def load_dotenv(cls) -> None:
        """Carga simple de clave=valor desde backend/.env (no pisa el entorno)."""
        if not cls.ENV_FILE.exists():
            return
        for raw_line in cls.ENV_FILE.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    @staticmethod
    def get(name: str, default=None):
        value = os.environ.get(name)
        return default if value in (None, "") else value

    @staticmethod
    def get_bool(name: str, default: bool = False) -> bool:
        value = os.environ.get(name)
        if value is None:
            return default
        return value.strip().lower() in ("1", "true", "yes", "on", "si")

    @staticmethod
    def get_int(name: str, default: int) -> int:
        try:
            return int(os.environ.get(name, default))
        except (TypeError, ValueError):
            return default

    @staticmethod
    def get_list(name: str, default=None) -> list:
        value = os.environ.get(name)
        if not value:
            return list(default or [])
        return [item.strip() for item in value.split(",") if item.strip()]


# El .env debe cargarse ANTES de leer cualquier variable, porque las clases
# siguientes resuelven sus valores en el momento de ser definidas.
Environment.load_dotenv()


class PathsConfig:
    """Rutas del proyecto."""

    BASE_DIR = BASE_DIR
    BACKEND_DIR = BACKEND_DIR
    FRONTEND_DIR = FRONTEND_DIR
    TEMPLATES_DIR = FRONTEND_DIR / "templates"
    STATIC_DIR = FRONTEND_DIR / "static"
    MEDIA_DIR = BACKEND_DIR / "media"


def _resolve_allowed_hosts(render_hostname: str) -> list:
    """Hosts admitidos, combinando el entorno con los valores por defecto.

    Siempre incluye localhost y 127.0.0.1 (desarrollo) y, si Render publico el
    servicio, tambien su RENDER_EXTERNAL_HOSTNAME. Se pueden agregar mas con
    DJANGO_ALLOWED_HOSTS, por ejemplo "*.onrender.com".
    """
    hosts = Environment.get_list("DJANGO_ALLOWED_HOSTS", [])
    for host in ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]:
        if host not in hosts:
            hosts.append(host)
    if render_hostname and render_hostname not in hosts:
        hosts.append(render_hostname)
    return hosts


def _resolve_csrf_trusted_origins(render_hostname: str) -> list:
    """Origenes de confianza para CSRF (con esquema incluido)."""
    origins = Environment.get_list(
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        ["http://localhost:8000", "http://127.0.0.1:8000"],
    )
    if render_hostname:
        https = f"https://{render_hostname}"
        if https not in origins:
            origins.append(https)
    return origins


class SecurityConfig:
    """Claves, hosts y modo debug."""

    # SECRET_KEY y DEBUG SIEMPRE vienen del entorno; nunca hay un valor real
    # escrito en el codigo.
    SECRET_KEY = Environment.get("DJANGO_SECRET_KEY", DEV_SECRET_KEY)
    DEBUG = Environment.get_bool("DJANGO_DEBUG", True)

    # Render lo define solo en el Web Service: es el dominio publico.
    # Ejemplo: "dockerize-abc123" -> "dockerize-abc123.onrender.com".
    RENDER_EXTERNAL_HOSTNAME = Environment.get("RENDER_EXTERNAL_HOSTNAME", "")

    SECURE_SSL_REDIRECT = Environment.get_bool("DJANGO_SECURE_SSL_REDIRECT", False)
    SESSION_COOKIE_SECURE = Environment.get_bool("DJANGO_SESSION_COOKIE_SECURE", False)
    CSRF_COOKIE_SECURE = Environment.get_bool("DJANGO_CSRF_COOKIE_SECURE", False)

    # Detras de un proxy inverso (el de Render) el esquema real llega en la
    # cabecera X-Forwarded-Proto, no en el socket.
    TRUST_X_FORWARDED_PROTO = Environment.get_bool("DJANGO_TRUST_X_FORWARDED_PROTO", False)

    ALLOWED_HOSTS = _resolve_allowed_hosts(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS = _resolve_csrf_trusted_origins(RENDER_EXTERNAL_HOSTNAME)


# Con DEBUG=False arrancar en produccion con una clave conocida seria un fallo
# de seguridad. Es preferible no arrancar a arrancar con una clave publica.
if not SecurityConfig.DEBUG and SecurityConfig.SECRET_KEY == DEV_SECRET_KEY:
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY debe estar definida en el entorno cuando "
        "DJANGO_DEBUG=False. Genera una con:\n"
        '    python -c "import secrets; print(secrets.token_urlsafe(64))"'
    )


class PostgreSQLConfig:
    """Parametros de conexion a PostgreSQL tomados del entorno.

    La fuente principal es DATABASE_URL (formato de Render). Si no existe, se
    arma la URL con las variables sueltas DB_HOST / DB_PORT / DB_NAME /
    DB_USER / DB_PASSWORD.
    """

    DEFAULT_PORT = 5432

    @classmethod
    def url(cls) -> str:
        """Devuelve la DSN de PostgreSQL, o "" si no hay ninguna configurada."""
        url = Environment.get("DATABASE_URL", "")
        if url:
            return url

        host = Environment.get("DB_HOST", "")
        if not host:
            return ""

        user = Environment.get("DB_USER", "")
        password = Environment.get("DB_PASSWORD", "")
        name = Environment.get("DB_NAME", "docker_basico")
        port = Environment.get("DB_PORT", cls.DEFAULT_PORT)
        # quote() evita que una contraseña con @ o / rompa la URL.
        credenciales = f"{quote(user, safe='')}:{quote(password, safe='')}@" if user else ""
        return f"postgresql://{credenciales}{host}:{port}/{name}"


class DatabaseConfig:
    """Configuracion de base de datos completa (PostgreSQL)."""

    # Sin variables de entorno el proyecto cae a SQLite, para que `manage.py`
    # siga siendo usable en una maquina sin base de datos levantada.
    SQLITE_URL = f"sqlite:///{(BACKEND_DIR / 'db.sqlite3').as_posix()}"

    # 600 s evita re-conectar en cada peticion; con Render es necesario porque
    # las conexiones se cortan cuando el servicio free se apaga.
    CONN_MAX_AGE = Environment.get_int("DB_CONN_MAX_AGE", 600)
    CONN_HEALTH_CHECKS = Environment.get_bool("DB_CONN_HEALTH_CHECKS", True)

    @classmethod
    def databases(cls) -> dict:
        """Construye DATABASES a partir de DATABASE_URL."""
        dsn = PostgreSQLConfig.url() or cls.SQLITE_URL
        config = dj_database_url.config(
            default=dsn,
            conn_max_age=cls.CONN_MAX_AGE,
            conn_health_checks=cls.CONN_HEALTH_CHECKS,
        )
        # dj-database-url solo agrega "OPTIONS" si la URL trae parametros
        # (por ejemplo ?sslmode=require). Django tambien la rellena, pero el
        # backend de PostgreSQL accede a settings_dict["OPTIONS"] de forma
        # directa, asi que se garantiza que la clave exista.
        config.setdefault("OPTIONS", {})
        if "sqlite" in config["ENGINE"]:
            # SQLite es un archivo local: mantener conexiones vivas entre
            # peticiones solo genera bloqueos.
            config["CONN_MAX_AGE"] = 0
            config["CONN_HEALTH_CHECKS"] = False
        return {"default": config}


class AppsConfig:
    """Apps instaladas y configuracion propia de cada app."""

    INSTALLED = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.humanize",
        "apps.core.apps.CoreConfig",
        "apps.accounts.apps.AccountsConfig",
    ]

    # Apps propias (se usan para resolver nombres largos en los templates)
    LOCAL_APPS = ["apps.core", "apps.accounts"]


class TemplatesConfig:
    """Rutas de templates (viven en el frontend)."""

    BACKEND = "django.template.backends.django.DjangoTemplates"

    @classmethod
    def context_processors(cls) -> list:
        return [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "apps.core.context_processors.site_context",
        ]

    @classmethod
    def options(cls) -> dict:
        return {
            "BACKEND": cls.BACKEND,
            "DIRS": [PathsConfig.TEMPLATES_DIR],
            "APP_DIRS": True,
            "OPTIONS": {"context_processors": cls.context_processors()},
        }


class StaticConfig:
    """Archivos estaticos (viven en el frontend)."""

    URL = "/static/"
    ROOT = PathsConfig.STATIC_DIR
    COLLECTED_DIR = BACKEND_DIR / "staticfiles"

    @classmethod
    def options(cls) -> dict:
        return {"BASE_DIR": cls.ROOT}


class AuthConfig:
    """Ajustes de autenticacion."""

    LOGIN_URL = "accounts:login"
    LOGIN_REDIRECT_URL = "core:home"
    LOGOUT_REDIRECT_URL = "core:home"


class InternationalizationConfig:
    LANGUAGE_CODE = "es"
    TIME_ZONE = "America/Bogota"
    USE_I18N = True
    USE_TZ = True


class Config:
    """Punto unico de acceso a la configuracion del proyecto."""

    PATHS = PathsConfig
    SECURITY = SecurityConfig
    DATABASES = DatabaseConfig
    APPS = AppsConfig
    TEMPLATES = TemplatesConfig
    STATIC = StaticConfig
    AUTH = AuthConfig
    I18N = InternationalizationConfig
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
