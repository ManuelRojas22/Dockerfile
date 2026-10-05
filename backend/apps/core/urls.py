"""Rutas de la app core (namespace: core)."""

from django.urls import path

from apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("quienes-somos/", views.AboutView.as_view(), name="about"),
    path("precios/", views.PricingListView.as_view(), name="pricing"),
    path("precios/<slug:slug>/", views.PlanDetailView.as_view(), name="plan_detail"),
    path("contacto/", views.ContactView.as_view(), name="contact"),
]
