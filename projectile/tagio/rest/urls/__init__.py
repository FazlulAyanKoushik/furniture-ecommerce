from django.urls import include, path

urlpatterns = [
    path("/categories", include("tagio.rest.urls.categories")),
]
