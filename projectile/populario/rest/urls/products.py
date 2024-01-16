from django.urls import path

from populario.rest.views.products import (
    GlobalPopularProductList,
)


urlpatterns = [
    path(
        r"",
        GlobalPopularProductList.as_view(),
        name="global.popular-product-list",
    ),
]
