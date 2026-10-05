"""Modelos del equipo (pagina 'Quienes somos')."""

from django.db import models

from apps.core.models.base import PublishedModel


class TeamMember(PublishedModel):
    """Integrante del equipo mostrado en la pagina institutional."""

    full_name = models.CharField("nombre completo", max_length=120)
    role = models.CharField("cargo", max_length=120)
    bio = models.TextField("biografia", blank=True)
    initials = models.CharField(
        "iniciales", max_length=4, help_text="Se usa como avatar de respaldo."
    )
    linkedin_url = models.URLField("LinkedIn", blank=True)
    github_url = models.URLField("GitHub", blank=True)

    class Meta(PublishedModel.Meta):
        verbose_name = "integrante"
        verbose_name_plural = "integrantes"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.role})"
