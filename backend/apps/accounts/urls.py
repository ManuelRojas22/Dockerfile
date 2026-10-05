"""Rutas de la app accounts (namespace: accounts)."""

from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("registro/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("perfil/", views.ProfileDetailView.as_view(), name="profile"),
    path("perfil/editar/", views.ProfileUpdateView.as_view(), name="profile_edit"),
]
