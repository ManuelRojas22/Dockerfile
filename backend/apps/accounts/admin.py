"""Administracion de perfiles."""

from django.contrib import admin

from apps.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "role", "created_at")
    search_fields = ("user__username", "user__email", "company")
    raw_id_fields = ("user",)
