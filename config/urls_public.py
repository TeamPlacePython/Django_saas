from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from apps.tenant_manager.admin import tenant_admin_site

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin_tenants/", tenant_admin_site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.home.urls", namespace="home")),
    path("profile/", include("apps.users.urls", namespace="users")),
]

# Only used when DEBUG=True, whitenoise can serve files when DEBUG=False
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
