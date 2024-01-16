"""projectile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Supplers",
        default_version="main",
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=[permissions.AllowAny],
)

# Change Admin Top Nav Header
admin.site.site_header = "Supplers Admin"

urlpatterns = [
    # Swagger
    re_path(
        r"^docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=10),
        name="schema-json",
    ),
    re_path(
        r"^docs/swagger$",
        schema_view.with_ui("swagger", cache_timeout=10),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^docs/redoc$",
        schema_view.with_ui("redoc", cache_timeout=10),
        name="schema-redoc",
    ),
    # JWT Token
    path(
        "api/v1/token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    # adio
    path("api/v1/ads", include("adio.rest.urls")),
    # adminio
    path("api/v1/admin", include("adminio.rest.urls")),
    # core public
    path("api/v1/verify", include("core.rest.urls.verify")),
    path("api/v1/public", include("publicapi.rest.urls")),
    # core private
    path("api/v1/me", include("core.rest.urls.me")),
    # accountio
    path("api/v1/organizations", include("accountio.rest.urls.organizations")),
    # catalogio
    path("api/v1", include("catalogio.rest.urls")),
    path("api/v1/brands", include("catalogio.rest.urls.brands")),
    # collabio
    path("api/v1/projects", include("collabio.rest.urls.projects")),
    # gruppio
    path("api/v1/groups", include("gruppio.rest.urls.groups")),
    # invites
    path("api/v1/invites", include("invitio.rest.urls")),
    # search
    path("api/v1/search", include("search.rest.urls")),
    # paymentio subscription plan apis
    path("api/v1/subscription-plans", include("paymentio.rest.urls.subscription_plan")),
    # populario
    path("api/v1/popular", include("populario.rest.urls")),
    # scrapio
    # path("api/v1/scrap", include("scrapio.rest.urls")),
    # weapi apis
    path("api/v1/tags", include("tagio.rest.urls")),
    # weapi apis
    path("api/v1/we", include("weapi.rest.urls")),
    # collabio
    # path("api/v1", include("collabio.rest.urls")),
    # admin
    path("adminium/", admin.site.urls),
    # django-health-check urls
    path("health/", include("health_check.urls")),
    # contentio
    path("api/v1/faqs", include("contentio.rest.urls.faqs")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # debug_tool_url = [path('__debug__/', include('debug_toolbar.urls'))]
    # urlpatterns += debug_tool_url
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
