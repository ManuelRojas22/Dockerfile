"""Vistas de la app core, todas basadas en clases."""

from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView, TemplateView, View

from apps.core.forms import ContactForm
from apps.core.services import (
    AboutContentService,
    ContactService,
    DockerContentService,
    PlanService,
    SiteContextService,
)


class SiteContextMixin:
    """Inyecta datos globales del sitio a todos los templates."""

    site_service = SiteContextService

    def get_site_context(self) -> dict:
        return {
            "site_name": self.site_service.site_name(),
            "site_tagline": self.site_service.tagline(),
            "nav_links": self.site_service.nav_links(),
            "footer_links": self.site_service.footer_links(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_site_context())
        return context


class HomeView(SiteContextMixin, TemplateView):
    """Pagina inicial: explicacion de que es Docker."""

    template_name = "index.html"
    content_service = DockerContentService

    def get_context_data(self, **kwargs):
        content = self.content_service.home_content()
        context = {
            "hero": content.hero,
            "stats": content.stats,
            "features": content.features,
            "steps": content.steps,
            "code_example": content.code_example,
            "faq": content.faq,
            "starting_price": PlanService.starting_price_display(),
            "contact_form": ContactForm(),
        }
        return super().get_context_data(**kwargs, **context)


class AboutView(SiteContextMixin, TemplateView):
    """Pagina 'Quienes somos'."""

    template_name = "quienes_somos.html"
    content_service = AboutContentService

    def get_context_data(self, **kwargs):
        context = {
            "header": self.content_service.header(),
            "mission": self.content_service.mission(),
            "values": self.content_service.values(),
            "milestones": self.content_service.milestones(),
            "team": self.content_service.team(),
        }
        return super().get_context_data(**kwargs, **context)


class PricingListView(SiteContextMixin, TemplateView):
    """Pagina de precios."""

    template_name = "precios.html"

    def get_context_data(self, **kwargs):
        plans = PlanService.list_plans()
        context = {
            "plans": plans,
            "featured_plan": PlanService.featured_plan(),
            "features_by_plan": {plan.pk: PlanService.features_of(plan) for plan in plans},
            "has_plans": bool(plans),
        }
        return super().get_context_data(**kwargs, **context)


class PlanDetailView(SiteContextMixin, DetailView):
    """Detalle de un plan."""

    template_name = "plan_detalle.html"
    context_object_name = "plan"

    def get_queryset(self):
        return PlanService.all_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plan_features"] = PlanService.features_of(self.object)
        context["other_plans"] = [
            plan for plan in PlanService.list_plans() if plan.pk != self.object.pk
        ]
        return context


class ContactView(SiteContextMixin, View):
    """Recibe el formulario de contacto por POST."""

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactService.send(**form.cleaned_data)
            messages.success(request, "Gracias por escribirnos, responderemos pronto.")
        else:
            messages.error(request, "Revisa los datos del formulario.")
        return redirect(request.POST.get("next") or "core:home")

    def get(self, request, *args, **kwargs):
        return redirect("core:home")


class NotFoundView(SiteContextMixin, TemplateView):
    """Pagina 404."""

    template_name = "404.html"
    status_code = 404

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = self.status_code
        return super().render_to_response(context, **response_kwargs)


class ServerErrorView(TemplateView):
    """Pagina 500."""

    template_name = "500.html"
    status_code = 500

    def render_to_response(self, context, **response_kwargs):
        response_kwargs["status"] = self.status_code
        return super().render_to_response(context, **response_kwargs)


# --- Funciones que Django resuelve por nombre en config/urls.py -----------
def page_not_found(request, exception=None):
    return NotFoundView.as_view()(request, exception=exception)


def server_error(request):
    return ServerErrorView.as_view()(request)
