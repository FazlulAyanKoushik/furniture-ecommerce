from django.urls import path, include


urlpatterns = [
    path(r"/sales-login", include("adminio.rest.urls.login")),
    path(r"", include("adminio.rest.urls.dashboard")),
]
