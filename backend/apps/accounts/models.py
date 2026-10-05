"""Perfil de usuario (modelo propio enlazado a auth.User)."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Datos extra del usuario (1:1 con el usuario nativo de Django)."""

    user = models.OneToOneField(
        User,
        verbose_name="usuario",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    company = models.CharField("empresa", max_length=120, blank=True)
    role = models.CharField("cargo", max_length=120, blank=True)
    bio = models.TextField("biografia", blank=True)
    avatar_url = models.URLField("avatar", blank=True)
    created_at = models.DateTimeField("creado en", auto_now_add=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self) -> str:
        return f"Perfil de {self.user.get_username()}"

    def get_absolute_url(self) -> str:
        return reverse("accounts:profile")

    @property
    def display_name(self) -> str:
        return self.user.get_full_name() or self.user.get_username()

    @property
    def initials(self) -> str:
        source = self.display_name.strip()
        parts = [part for part in source.split() if part]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()
