"""Capa de servicios: toda la logica de negocio vive aqui.

Las vistas solo orquestan (request -> servicio -> contexto -> template).
Cada servicio es una clase con metodos de clase, sin estado global.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from apps.core.models import ContactMessage, Plan, PlanFeature, TeamMember


# ---------------------------------------------------------------------------
# Estructuras simples de solo lectura para el contenido estatico
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FeatureItem:
    icon: str
    title: str
    text: str


@dataclass(frozen=True)
class StepItem:
    number: str
    title: str
    text: str


@dataclass(frozen=True)
class StatItem:
    value: str
    label: str


@dataclass(frozen=True)
class FaqItem:
    question: str
    answer: str


@dataclass(frozen=True)
class ValueItem:
    title: str
    text: str


@dataclass(frozen=True)
class MilestoneItem:
    year: str
    title: str
    text: str


@dataclass(frozen=True)
class HomeContent:
    """Todo el contenido de la pagina inicial en un solo objeto."""

    hero: dict = field(default_factory=dict)
    stats: Iterable[StatItem] = ()
    features: Iterable[FeatureItem] = ()
    steps: Iterable[StepItem] = ()
    code_example: dict = field(default_factory=dict)
    faq: Iterable[FaqItem] = ()


# ---------------------------------------------------------------------------
# Contenido editorial sobre Docker
# ---------------------------------------------------------------------------
class DockerContentService:
    """Fuente unica del contenido que explica que es Docker."""

    HERO = {
        "badge": "Docker 24+ / Contenedores",
        "title": "Que es Docker",
        "subtitle": (
            "Empaqueta tu aplicacion, sus dependencias y su sistema de archivos "
            "en una imagen reproducible que se ejecuta igual en tu equipo, en "
            "servidores y en la nube."
        ),
        "description": (
            "Docker es una plataforma de contenedores: una forma ligera de aislar "
            "procesos del sistema operativo en lugar de virtualizar hardware completo. "
            "Cada contenedor arranca en segundos, comparte el kernel del host y se "
            "distribuye como un artefacto unico y reproducible."
        ),
        "primary_cta": {"text": "Ver precios", "target": "core:pricing"},
        "secondary_cta": {"text": "Quienes somos", "target": "core:about"},
    }

    STATS = [
        StatItem(value="+30M", label="contenedores descargados por mes"),
        StatItem(value="99.9%", label="disponibilidad en Docker Hub"),
        StatItem(value="~1s", label="arranque tipico de un contenedor"),
        StatItem(value="1 archivo", label="Dockerfile como fuente de verdad"),
    ]

    FEATURES = [
        FeatureItem(
            icon="box",
            title="Imagenes inmutables",
            text="Cada build produce una imagen con hash reproducible y capas cacheadas.",
        ),
        FeatureItem(
            icon="bolt",
            title="Arranque instantaneo",
            text="Los procesos aíslados comparten kernel: no hay boot de sistema completo.",
        ),
        FeatureItem(
            icon="layers",
            title="Capas en cache",
            text="Solo se reenvian las capas que cambiaron, builds en segundos.",
        ),
        FeatureItem(
            icon="shield",
            title="Aislamiento seguro",
            text="Namespaces, cgroups y capacidades mínimas por contenedor.",
        ),
        FeatureItem(
            icon="rocket",
            title="Portable",
            text="El mismo contenedor corre en Linux, macOS, Windows y Kubernetes.",
        ),
        FeatureItem(
            icon="scale",
            title="Escalable",
            text="Orquesta miles de instancias con docker compose o Kubernetes.",
        ),
    ]

    STEPS = [
        StepItem(
            number="01",
            title="Escribes el Dockerfile",
            text="Describes la imagen, el sistema base y el comando de arranque.",
        ),
        StepItem(
            number="02",
            title="Construyes la imagen",
            text="docker build genera capas cacheadas y un identificador unico.",
        ),
        StepItem(
            number="03",
            title="Ejecutas el contenedor",
            text="docker run levanta el proceso aislado con puertos y volumenes.",
        ),
        StepItem(
            number="04",
            title="Publicas y orquestas",
            text="Sube la imagen a un registro y escala con compose o Kubernetes.",
        ),
    ]

    CODE_EXAMPLE = {
        "language": "dockerfile",
        "filename": "Dockerfile",
        "lines": [
            "# 1. Imagen base minima",
            "FROM python:3.13-slim",
            "",
            "WORKDIR /app",
            "",
            "# 2. Copiar dependencias (capa cacheada)",
            "COPY requirements.txt .",
            "RUN pip install --no-cache-dir -r requirements.txt",
            "",
            "# 3. Copiar el codigo y exponer el puerto",
            "COPY . .",
            "EXPOSE 8000",
            "",
            "# 4. Comando por defecto",
            'CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]',
        ],
        "commands": [
            "docker build -t mi-app .",
            "docker run -p 8000:8000 mi-app",
            "docker ps",
            "docker logs -f <container_id>",
        ],
    }

    FAQ = [
        FaqItem(
            question="Docker no es lo mismo que una maquina virtual?",
            answer=(
                "Una VM emula hardware y corre un sistema operativo completo. "
                "Un contenedor isolate solo el proceso y comparte el kernel del host, "
                "por eso pesa megabytes y arranca en segundos."
            ),
        ),
        FaqItem(
            question="Que diferencia hay entre imagen y contenedor?",
            answer=(
                "La imagen es la plantilla de solo lectura; el contenedor es la "
                "instancia en ejecucion de esa imagen. Puedes tener N contenedores "
                "a partir de la misma imagen."
            ),
        ),
        FaqItem(
            question="Que es un volumen en Docker?",
            answer=(
                "Es un almacenamiento persistente fuera del ciclo de vida del "
                "contenedor. Sirve para conservar datos de bases de datos o archivos "
                "subidos por el usuario."
            ),
        ),
        FaqItem(
            question="Necesito Docker en mi PC de desarrollo?",
            answer=(
                "No. Docker empaqueta y despliega; para desarrollo puedes instalar "
                "las dependencias en tu sistema y usar Docker solo para el despliegue."
            ),
        ),
    ]

    @classmethod
    def home_content(cls) -> HomeContent:
        return HomeContent(
            hero=cls.HERO,
            stats=cls.STATS,
            features=cls.FEATURES,
            steps=cls.STEPS,
            code_example=cls.CODE_EXAMPLE,
            faq=cls.FAQ,
        )


class AboutContentService:
    """Contenido de la pagina 'Quienes somos'."""

    HEADER = {
        "badge": "Sobre nosotros",
        "title": "Quienes somos",
        "subtitle": (
            "Ayudamos a equipos de desarrollo a entregar software rapido y "
            "reproducible usando contenedores como base de su infraestructura."
        ),
    }

    MISSION = (
        "Creemos que la infraestructura tambien es codigo. Por eso construimos "
        "herramientas y acompanamos a equipos para que desplieguen sin sorpresas, "
        "con procesos reproducibles y documentados."
    )

    VALUES = [
        ValueItem(
            title="Reproducibilidad",
            text="Si funciona en tu maquina, funciona en produccion. Siempre.",
        ),
        ValueItem(
            title="Simplicidad",
            text="Si una infraestructura necesita 200 pasos, todavia hay que simplificarla.",
        ),
        ValueItem(
            title="Aprendizaje",
            text="Documentamos lo que aprendemos y lo compartimos con la comunidad.",
        ),
        ValueItem(
            title="Colaboracion",
            text="Codigo abierto, revisiones honestas y decisiones documentadas.",
        ),
    ]

    MILESTONES = [
        MilestoneItem(
            year="2021",
            title="Fundacion del equipo",
            text="Cuatro ingenieros, una idea: desplegar sin servidor de por medio.",
        ),
        MilestoneItem(
            year="2023",
            title="Primera plataforma",
            text="Automaticamos el pipeline con contenedores y registries privados.",
        ),
        MilestoneItem(
            year="2025",
            title="Comunidad abierta",
            text="Publicamos guias y herramientas usadas por mas de 1.000 equipos.",
        ),
    ]

    @classmethod
    def header(cls) -> dict:
        return cls.HEADER

    @classmethod
    def mission(cls) -> str:
        return cls.MISSION

    @classmethod
    def values(cls) -> list[ValueItem]:
        return list(cls.VALUES)

    @classmethod
    def milestones(cls) -> list[MilestoneItem]:
        return list(cls.MILESTONES)

    @classmethod
    def team(cls) -> list[TeamMember]:
        return list(TeamMember.objects.filter(is_active=True))


class SiteContextService:
    """Datos globales que el navbar y el footer necesitan."""

    SITE_NAME = "Dockerize"
    TAGLINE = "Contenedores para equipos que despliegan rapido"

    @classmethod
    def site_name(cls) -> str:
        return cls.SITE_NAME

    @classmethod
    def tagline(cls) -> str:
        return cls.TAGLINE

    @classmethod
    def nav_links(cls) -> list[dict]:
        return [
            {"label": "Inicio", "url_name": "core:home", "view_name": "home"},
            {"label": "Quienes somos", "url_name": "core:about", "view_name": "about"},
            {"label": "Precios", "url_name": "core:pricing", "view_name": "pricing"},
        ]

    @classmethod
    def footer_links(cls) -> list[dict]:
        return cls.nav_links()


# ---------------------------------------------------------------------------
# Servicios con acceso a base de datos
# ---------------------------------------------------------------------------
class PlanService:
    """Reglas de negocio de la pagina de precios."""

    @classmethod
    def all_queryset(cls):
        """Queryset de planes activos con sus caracteristicas precargadas."""
        return Plan.objects.activos().prefetch_related("features")

    @classmethod
    def list_plans(cls) -> list[Plan]:
        return list(Plan.objects.activos().prefetch_related("features"))

    @classmethod
    def featured_plan(cls) -> Plan | None:
        return Plan.objects.destacados().first()

    @classmethod
    def get_plan(cls, slug: str) -> Plan | None:
        return (
            Plan.objects.activos()
            .prefetch_related("features")
            .filter(slug=slug)
            .first()
        )

    @classmethod
    def features_of(cls, plan: Plan) -> list[PlanFeature]:
        return [feature for feature in plan.features.all() if feature.is_active]

    @classmethod
    def cheapest(cls) -> Plan | None:
        return Plan.objects.activos().order_by("price_monthly").first()

    @classmethod
    def starting_price_display(cls) -> str:
        plan = cls.cheapest()
        return plan.monthly_price_display if plan else "Contactanos"


class ContactService:
    """Persistencia de mensajes de contacto."""

    @classmethod
    def send(cls, *, name: str, email: str, subject: str, message: str) -> ContactMessage:
        return ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

    @classmethod
    def unread_count(cls) -> int:
        return ContactMessage.objects.filter(is_read=False).count()
