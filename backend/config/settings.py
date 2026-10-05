"""Configuracion Django del proyecto.

La logica de configuracion vive en `config/conf.py` (POO); aqui solo se
exponen los valores con los nombres que Django resuelve a nivel de modulo.
"""

from config.conf import Config

# --- Paths -----------------------------------------------------------------
BASE_DIR = Config.PATHS.BASE_DIR
BACKEND_DIR = Config.PATHS.BACKEND_DIR
FRONTEND_DIR = Config.PATHS.FRONTEND_DIR
MEDIA_ROOT = Config.PATHS.MEDIA_DIR
MEDIA_URL = "/media/"

# --- Seguridad -------------------------------------------------------------
SECRET_KEY = Config.SECURITY.SECRET_KEY
DEBUG = Config.SECURITY.DEBUG
ALLOWED_HOSTS = Config.SECURITY.ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS = Config.SECURITY.CSRF_TRUSTED_ORIGINS
SECURE_SSL_REDIRECT = Config.SECURITY.SECURE_SSL_REDIRECT
SESSION_COOKIE_SECURE = Config.SECURITY.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = Config.SECURITY.CSRF_COOKIE_SECURE

# --- Apps ------------------------------------------------------------------
INSTALLED_APPS = Config.APPS.INSTALLED
LOCAL_APPS = Config.APPS.LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Sirve /static/ dentro del contenedor (con DEBUG=False no hay runserver).
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Base de datos (MySQL) -------------------------------------------------
DATABASES = Config.DATABASES.databases()

# --- Templates y estaticos (frontend) --------------------------------------
TEMPLATES = [Config.TEMPLATES.options()]
STATIC_URL = Config.STATIC.URL
STATICFILES_DIRS = [Config.STATIC.ROOT]
STATIC_ROOT = Config.STATIC.COLLECTED_DIR
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG
        else "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

# --- Autenticacion ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGIN_URL = Config.AUTH.LOGIN_URL
LOGIN_REDIRECT_URL = Config.AUTH.LOGIN_REDIRECT_URL
LOGOUT_REDIRECT_URL = Config.AUTH.LOGOUT_REDIRECT_URL

# --- Internacionalizacion ---------------------------------------------------
LANGUAGE_CODE = Config.I18N.LANGUAGE_CODE
TIME_ZONE = Config.I18N.TIME_ZONE
USE_I18N = Config.I18N.USE_I18N
USE_TZ = Config.I18N.USE_TZ

DEFAULT_AUTO_FIELD = Config.DEFAULT_AUTO_FIELD

# --- Mensajes de error a espanol ------------------------------------------
from django.contrib.messages import constants as messages  # noqa: E402

MESSAGE_TAGS = {
    messages.DEBUG: "info",
    messages.INFO: "info",
    messages.SUCCESS: "exito",
    messages.WARNING: "alerta",
    messages.ERROR: "error",
}
