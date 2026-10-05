"""Modelos de planes y precios."""

from django.db import models
from django.urls import reverse

from apps.core.models.base import PublishedModel


class PlanQuerySet(models.QuerySet):
    """Consultas reutilizables sobre los planes."""

    def activos(self):
        return self.filter(is_active=True)

    def destacados(self):
        return self.activos().filter(is_featured=True)

    def con_precio(self):
        return self.activos().exclude(price_monthly=0)


class Plan(PublishedModel):
    """Plan de precios comercializado en la pagina de precios."""

    name = models.CharField("nombre", max_length=80)
    slug = models.SlugField("slug", max_length=80, unique=True)
    tagline = models.CharField("eslogan", max_length=140)
    description = models.TextField("descripcion", blank=True)

    price_monthly = models.DecimalField(
        "precio mensual", max_digits=10, decimal_places=2, default=0
    )
    price_yearly = models.DecimalField(
        "precio anual", max_digits=10, decimal_places=2, default=0
    )
    currency = models.CharField("moneda", max_length=4, default="USD")

    badge = models.CharField("etiqueta", max_length=40, blank=True)
    is_featured = models.BooleanField("destacado", default=False)

    objects = PlanQuerySet.as_manager()

    class Meta(PublishedModel.Meta):
        verbose_name = "plan"
        verbose_name_plural = "planes"
        ordering = ["order", "price_monthly"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("core:plan_detail", kwargs={"slug": self.slug})

    # -- Propiedades de negocio ---------------------------------------------
    @property
    def monthly_price_display(self) -> str:
        return self._format_price(self.price_monthly)

    @property
    def yearly_price_display(self) -> str:
        return self._format_price(self.price_yearly)

    @property
    def is_free(self) -> bool:
        return self.price_monthly == 0

    @property
    def annual_savings_percent(self) -> int:
        """Porcentaje de ahorro anual frente al pago mes a mes."""
        if self.is_free or not self.price_monthly:
            return 0
        full_year = self.price_monthly * 12
        if full_year <= 0 or self.price_yearly >= full_year:
            return 0
        return round((1 - (self.price_yearly / full_year)) * 100)

    def _format_price(self, value) -> str:
        if value == 0:
            return "Gratis"
        return f"{value:,.0f} {self.currency}"


class PlanFeature(PublishedModel):
    """Caracteristica incluida en un plan."""

    plan = models.ForeignKey(
        Plan,
        verbose_name="plan",
        on_delete=models.CASCADE,
        related_name="features",
    )
    title = models.CharField("titulo", max_length=120)
    description = models.CharField("detalle", max_length=200, blank=True)
    is_highlighted = models.BooleanField("destacada", default=False)

    class Meta(PublishedModel.Meta):
        verbose_name = "caracteristica de plan"
        verbose_name_plural = "caracteristicas de plan"
        ordering = ["plan_id", "order", "id"]

    def __str__(self) -> str:
        return f"{self.plan.name} - {self.title}"
