"""Context processors globales de la app core."""

from apps.core.services import SiteContextService


def site_context(request):
    """Variables disponibles en todos los templates sin pasar por la vista."""
    return {
        "site_name": SiteContextService.site_name(),
        "site_tagline": SiteContextService.tagline(),
        "nav_links": SiteContextService.nav_links(),
        "footer_links": SiteContextService.footer_links(),
    }
