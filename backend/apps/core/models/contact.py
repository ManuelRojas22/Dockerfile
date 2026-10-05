"""Modelo de mensajes de contacto."""

from django.db import models

from apps.core.models.base import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """Mensaje enviado desde el formulario de contacto."""

    name = models.CharField("nombre", max_length=120)
    email = models.EmailField("correo electronico")
    subject = models.CharField("asunto", max_length=160)
    message = models.TextField("mensaje")
    is_read = models.BooleanField("leido", default=False)

    class Meta:
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} - {self.email}"

    def mark_as_read(self) -> None:
        self.is_read = True
        self.save(update_fields=["is_read"])
