"""Registro de modelos en el panel de administracion."""

from django.contrib import admin

from apps.core.models import ContactMessage, Plan, PlanFeature, TeamMember


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    fields = ("title", "description", "is_highlighted", "is_active", "order")


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price_monthly", "price_yearly", "badge", "is_featured", "is_active")
    list_filter = ("is_active", "is_featured")
    search_fields = ("name", "tagline", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PlanFeatureInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("full_name", "role", "bio")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at", "updated_at")
    actions = ["marcar_como_leidos"]

    @admin.action(description="Marcar como leidos")
    def marcar_como_leidos(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} mensaje(s) marcado(s) como leidos.")
