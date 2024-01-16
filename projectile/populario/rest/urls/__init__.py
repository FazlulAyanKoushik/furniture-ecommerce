from django.urls import include, path


urlpatterns = [
    path("/organizations", include("populario.rest.urls.organizations")),
    path("/products", include("populario.rest.urls.products")),
    path("/projects", include("populario.rest.urls.projects")),
]
