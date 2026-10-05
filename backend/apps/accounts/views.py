"""Vistas de cuentas: registro, login, logout y perfil (todas CBV)."""

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, TemplateView, UpdateView

from apps.accounts.forms import LoginForm, ProfileForm, RegisterForm
from apps.accounts.models import Profile
from apps.accounts.services import AccountService
from apps.core.services import SiteContextService


class SiteContextMixin:
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


class RegisterView(SiteContextMixin, CreateView):
    """Formulario de registro."""

    template_name = "auth/registro.html"
    form_class = RegisterForm
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Crear cuenta"
        context["auth_mode"] = "registro"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        # `self.object` ya fue guardado por CreateView: queda con sesion iniciada.
        auth_login(
            self.request,
            self.object,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        messages.success(self.request, "Cuenta creada correctamente. Bienvenido.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "No pudimos crear la cuenta, revisa los datos.")
        return super().form_invalid(form)


class LoginView(SiteContextMixin, FormView):
    """Inicio de sesion."""

    template_name = "auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Iniciar sesion"
        context["auth_mode"] = "login"
        return context

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        AccountService.get_or_create_profile(user)
        messages.success(self.request, f"Sesion iniciada como {user.get_username()}.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LogoutView(SiteContextMixin, RedirectView):
    """Cierre de sesion (solo POST)."""

    permanent = False
    pattern_name = "core:home"

    def post(self, request, *args, **kwargs):
        auth_logout(request)
        messages.info(request, "Sesion cerrada correctamente.")
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.warning(request, "Usa el boton de salida para cerrar sesion.")
        return super().get(request, *args, **kwargs)


class ProfileDetailView(LoginRequiredMixin, SiteContextMixin, TemplateView):
    """Perfil del usuario en sesion."""

    template_name = "auth/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Mi perfil"
        context["profile"] = AccountService.get_or_create_profile(self.request.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, SiteContextMixin, UpdateView):
    """Edicion del perfil del usuario en sesion."""

    model = Profile
    form_class = ProfileForm
    template_name = "auth/perfil_editar.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return AccountService.get_or_create_profile(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar perfil"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Perfil actualizado.")
        return super().form_valid(form)
