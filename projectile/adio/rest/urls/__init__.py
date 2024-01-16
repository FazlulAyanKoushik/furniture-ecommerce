from django.urls import include, path

urlpatterns = [
    path("/products", include("adio.rest.urls.products")),
    path("/projects", include("adio.rest.urls.projects")),
    path("/organizations", include("adio.rest.urls.organizations")),
]
