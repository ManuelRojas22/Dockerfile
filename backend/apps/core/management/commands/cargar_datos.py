"""Comando: carga datos iniciales de planes y equipo.

Uso:
    python manage.py cargar_datos
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import Plan, PlanFeature, TeamMember


class Command(BaseCommand):
    help = "Carga planes de ejemplo y miembros del equipo (idempotente)."

    @transaction.atomic
    def handle(self, *args, **options):
        self._crear_planes()
        self._crear_equipo()
        self.stdout.write(self.style.SUCCESS("Datos iniciales cargados."))

    # -- Planes --------------------------------------------------------------
    def _crear_planes(self):
        planes = [
            {
                "order": 1,
                "name": "Hobby",
                "slug": "hobby",
                "tagline": "Para aprender Docker sin tarjeta de credito.",
                "description": "Todo lo necesario para construir tus primeras imagenes y probarlas localmente.",
                "price_monthly": 0,
                "price_yearly": 0,
                "badge": "Gratis",
                "is_featured": False,
                "features": [
                    ("1 proyecto activo", False),
                    ("Imagenes ilimitadas en builds locales", False),
                    ("Docker Compose basico", False),
                    ("Documentacion de inicio", True),
                    ("Soporte por comunidad", False),
                ],
            },
            {
                "order": 2,
                "name": "Pro",
                "slug": "pro",
                "tagline": "Para equipos que despliegan todas las semanas.",
                "description": "Registros privados, CI/CD con cache de capas y despliegue sin friccion.",
                "price_monthly": 29,
                "price_yearly": 290,
                "badge": "Mas popular",
                "is_featured": True,
                "features": [
                    ("10 proyectos activos", True),
                    ("Registros privados con escaneo de imagenes", True),
                    ("CI/CD con cache de capas", True),
                    ("Despliegues ilimitados", True),
                    ("Logs agregados por 30 dias", True),
                    ("Soporte prioritario en 24h", False),
                ],
            },
            {
                "order": 3,
                "name": "Enterprise",
                "slug": "enterprise",
                "tagline": "Para organizaciones con requisitos de cumplimiento.",
                "description": "SSO, auditoria, alta disponibilidad y soporte dedicado con SLA.",
                "price_monthly": 99,
                "price_yearly": 990,
                "badge": "Negocio",
                "is_featured": False,
                "features": [
                    ("Proyectos ilimitados", True),
                    ("SSO SAML / OIDC y roles granulares", True),
                    ("Registro de auditoria", True),
                    ("Alta disponibilidad y DR", True),
                    ("Cuenta dedicada y SLA 99.9%", True),
                    ("Consultoria de arquitectura", False),
                ],
            },
        ]

        for data in planes:
            features = data.pop("features")
            plan, created = Plan.objects.update_or_create(
                slug=data["slug"], defaults=data
            )
            plan.features.all().delete()
            for index, (title, highlighted) in enumerate(features, start=1):
                PlanFeature.objects.create(
                    plan=plan,
                    title=title,
                    is_highlighted=highlighted,
                    order=index,
                    is_active=True,
                )
            estado = "creado" if created else "actualizado"
            self.stdout.write(f"  - Plan '{plan.name}' {estado}")

    # -- Equipo --------------------------------------------------------------
    def _crear_equipo(self):
        miembros = [
            {
                "order": 1,
                "full_name": "Laura Mendoza",
                "role": "Cofundadora / Backend",
                "initials": "LM",
                "bio": "Dieciocho anos construyendo APIs. Escribe los servicios que sostienen este sitio.",
                "linkedin_url": "https://www.linkedin.com/",
                "github_url": "https://github.com/",
            },
            {
                "order": 2,
                "full_name": "Carlos Rincon",
                "role": "Cofundador / Plataforma",
                "initials": "CR",
                "bio": "Automatiza pipelines y registries. Obsesionado con builds reproducibles.",
                "linkedin_url": "https://www.linkedin.com/",
                "github_url": "https://github.com/",
            },
            {
                "order": 3,
                "full_name": "Ana Torres",
                "role": "Frontend",
                "initials": "AT",
                "bio": "Traduce ideas a interfaces. Cree en que el rendimiento tambien es diseno.",
                "linkedin_url": "https://www.linkedin.com/",
                "github_url": "",
            },
            {
                "order": 4,
                "full_name": "Diego Salinas",
                "role": "SRE",
                "initials": "DS",
                "bio": "Guardia de produccion: alertas, metricas y despliegues sin sustos a las 3 AM.",
                "linkedin_url": "https://www.linkedin.com/",
                "github_url": "",
            },
        ]

        for data in miembros:
            _, created = TeamMember.objects.update_or_create(
                full_name=data["full_name"], defaults=data
            )
            estado = "creado" if created else "actualizado"
            self.stdout.write(f"  - Integrante '{data['full_name']}' {estado}")
