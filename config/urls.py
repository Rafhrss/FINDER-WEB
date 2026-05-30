from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(("api.v1.urls", "api"), namespace="v1")),
    path(
        "accounts/login/",
        RedirectView.as_view(pattern_name="web:login", permanent=False),
    ),
    path(
        "accounts/signup/",
        RedirectView.as_view(pattern_name="web:login", permanent=False),
    ),
    path("accounts/", include("allauth.urls")),
    path("", include(("web.urls", "web"), namespace="web")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
