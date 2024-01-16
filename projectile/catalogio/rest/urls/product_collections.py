from django.urls import path

from ..views.products import (
    GlobalProductCollectionList,
    GlobalProductCollectionDetail,
    GlobalCollectionProductList,
)


urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalProductCollectionDetail.as_view(),
        name="products.collection-detail",
    ),
    path(
        r"/<slug:slug>/products",
        GlobalCollectionProductList.as_view(),
        name="products.collection-product-list",
    ),
    path(r"", GlobalProductCollectionList.as_view(), name="products.collection-list"),
]
