from django.urls import path

from ..views import products


urlpatterns = [
    path(
        r"/<slug:slug>/images",
        products.GlobalProductImageList.as_view(),
        name="products.product_image-list",
    ),
    path(
        r"/<slug:product_slug>/images/<uuid:image_uid>",
        products.GlobalProductImageDetail.as_view(),
        name="products.product_image-detail",
    ),
    path(
        r"/<slug:slug>/files",
        products.GlobalProductFileList.as_view(),
        name="products.product-file-list",
    ),
    path(
        r"/<slug:slug>",
        products.GlobalProductDetail.as_view(),
        name="products.product-detail",
    ),
    path(r"", products.GlobalProductList.as_view(), name="products.product-list"),
]
