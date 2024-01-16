from django.urls import path, include

urlpatterns = [
    path(r"/products", include("catalogio.rest.urls.products")),
    path(r"/collections", include("catalogio.rest.urls.product_collections")),
    path(r"/services", include("catalogio.rest.urls.services")),
]
