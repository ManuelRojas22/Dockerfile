"""URLs raiz del proyecto.

Cada app expone sus propias rutas en su `urls.py` con un `namespace`,
de modo que aqui solo se enganchan las apps.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("cuentas/", include("apps.accounts.urls", namespace="accounts")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Paginas de error propias del frontend
handler404 = "apps.core.views.page_not_found"
handler500 = "apps.core.views.server_error"
