from django.urls import path

from ..views.products import GlobalProductAdsList, GlobalProductAdDetail


urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalProductAdDetail.as_view(),
        name="global.product-ads-detail",
    ),
    path(
        r"",
        GlobalProductAdsList.as_view(),
        name="global.product-ads-list",
    ),
]
