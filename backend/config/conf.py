"""Configuracion del proyecto resuelta desde el entorno, en POO.

Este modulo centraliza toda la configuracion "dura" del proyecto en clases.
`settings.py` solo se limita a exponer estos valores con los nombres que
Django espera a nivel de modulo.
"""

import os
from pathlib import Path

# Raiz del proyecto: .../proyecto basico
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Raiz del backend: .../proyecto basico/backend
BACKEND_DIR = BASE_DIR / "backend"

# Raiz del frontend: .../proyecto basico/frontend
FRONTEND_DIR = BASE_DIR / "frontend"


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


class SecurityConfig:
    """Claves, hosts y modo debug."""

    SECRET_KEY = Environment.get(
        "DJANGO_SECRET_KEY", "django-insecure-clave-de-desarrollo-cambiar-en-produccion"
    )
    DEBUG = Environment.get_bool("DJANGO_DEBUG", True)
    ALLOWED_HOSTS = Environment.get_list("DJANGO_ALLOWED_HOSTS", ["localhost", "127.0.0.1", "0.0.0.0", "testserver"])
    CSRF_TRUSTED_ORIGINS = Environment.get_list(
        "DJANGO_CSRF_TRUSTED_ORIGINS", ["http://localhost:8000", "http://127.0.0.1:8000"]
    )
    SECURE_SSL_REDIRECT = Environment.get_bool("DJANGO_SECURE_SSL_REDIRECT", False)
    SESSION_COOKIE_SECURE = Environment.get_bool("DJANGO_SESSION_COOKIE_SECURE", False)
    CSRF_COOKIE_SECURE = Environment.get_bool("DJANGO_CSRF_COOKIE_SECURE", False)


class MySQLConfig:
    """Parametros de conexion a MySQL."""

    ENGINE = "django.db.backends.mysql"
    NAME = Environment.get("MYSQL_DATABASE", "docker_basico")
    USER = Environment.get("MYSQL_USER", "root")
    PASSWORD = Environment.get("MYSQL_PASSWORD", "")
    HOST = Environment.get("MYSQL_HOST", "127.0.0.1")
    PORT = Environment.get("MYSQL_PORT", "3306")
    CONN_MAX_AGE = Environment.get_int("MYSQL_CONN_MAX_AGE", 60)

    @classmethod
    def options(cls) -> dict:
        """Opciones del charset para MySQL."""
        return {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }


class DatabaseConfig:
    """Configuracion de base de datos completa."""

    DEFAULT = {
        "ENGINE": MySQLConfig.ENGINE,
        "NAME": MySQLConfig.NAME,
        "USER": MySQLConfig.USER,
        "PASSWORD": MySQLConfig.PASSWORD,
        "HOST": MySQLConfig.HOST,
        "PORT": MySQLConfig.PORT,
        "CONN_MAX_AGE": MySQLConfig.CONN_MAX_AGE,
        "OPTIONS": MySQLConfig.options(),
        "TEST": {"CHARSET": "utf8mb4", "COLLATION": "utf8mb4_unicode_ci"},
    }

    @classmethod
    def databases(cls) -> dict:
        return {"default": cls.DEFAULT}


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
