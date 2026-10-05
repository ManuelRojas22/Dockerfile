"""Comando: crea la base de datos MySQL si todavia no existe.

Uso:
    python manage.py crear_base_datos
"""

import MySQLdb

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea la base de datos MySQL configurada en settings.py (si no existe)."

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        name = db["NAME"]

        try:
            connection = MySQLdb.connect(
                host=db["HOST"],
                port=int(db["PORT"] or 3306),
                user=db["USER"],
                password=db["PASSWORD"],
                charset="utf8mb4",
            )
        except MySQLdb.OperationalError as exc:
            raise CommandError(
                f"No se pudo conectar a MySQL en {db['HOST']}:{db['PORT']} -> {exc}"
            )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
                )
            self.stdout.write(self.style.SUCCESS(f"Base de datos '{name}' lista."))
        finally:
            connection.close()
