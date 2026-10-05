"""Modelos base reutilizables de la app core."""

from django.db import models


class TimeStampedModel(models.Model):
    """Modelo abstracto que agrega marcas de tiempo automaticas."""

    created_at = models.DateTimeField("creado en", auto_now_add=True)
    updated_at = models.DateTimeField("actualizado en", auto_now=True)

    class Meta:
        abstract = True


class PublishedModel(TimeStampedModel):
    """Modelo abstracto para contenido publicable y ordenable."""

    is_active = models.BooleanField("activo", default=True)
    order = models.PositiveSmallIntegerField("orden", default=0)

    class Meta:
        abstract = True
        ordering = ["order", "id"]
