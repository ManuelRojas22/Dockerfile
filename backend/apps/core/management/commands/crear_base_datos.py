"""Comando: crea la base de datos PostgreSQL si todavia no existe.

Uso:
    python manage.py crear_base_datos

En Render NO debes usar este comando: la base ya viene creada por el proveedor
y el entrypoint se limita a ejecutar `manage.py migrate`.
"""

import psycopg

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

# Base de mantenimiento a la que hay que conectarse para poder crear la final.
# Existe siempre en un PostgreSQL recien inicializado.
MAINTENANCE_DB = "postgres"


class Command(BaseCommand):
    help = "Crea la base de datos PostgreSQL configurada en settings.py (si no existe)."

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        engine = db["ENGINE"]

        if "sqlite" in engine:
            raise CommandError(
                "El proyecto esta usando SQLite (no hay DATABASE_URL definida): "
                "no hay ninguna base de datos que crear."
            )

        if "postgres" not in engine:
            raise CommandError(
                f"Este comando solo soporta PostgreSQL y el motor actual es {engine}."
            )

        name = db["NAME"]
        host = db.get("HOST") or ""
        port = int(db.get("PORT") or 5432)

        if not name:
            raise CommandError("La configuracion no define el nombre de la base de datos.")

        try:
            connection = psycopg.connect(
                host=host,
                port=port,
                dbname=MAINTENANCE_DB,
                user=db.get("USER") or "",
                password=db.get("PASSWORD") or "",
                connect_timeout=10,
                autocommit=True,
            )
        except psycopg.OperationalError as exc:
            raise CommandError(
                f"No se pudo conectar a PostgreSQL en {host}:{port} -> {exc}"
            )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s", (name,)
                )
                if cursor.fetchone():
                    self.stdout.write(
                        self.style.WARNING(f"La base de datos '{name}' ya existe.")
                    )
                    return

                # El nombre de una base es un identificador y los
                # identificadores no aceptan parametros, asi que se valida
                # antes de interpolarlo en el DDL.
                if not name.replace("_", "").isalnum():
                    raise CommandError(
                        f"Nombre de base de datos no permitido: {name!r}. "
                        "Usa solo letras, digitos y guion bajo."
                    )

                cursor.execute(f'CREATE DATABASE "{name}" ENCODING \'utf8\'')

            self.stdout.write(
                self.style.SUCCESS(f"Base de datos '{name}' creada.")
            )
        finally:
            connection.close()
