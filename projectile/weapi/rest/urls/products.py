from django.urls import path
from weapi.rest.views import products

urlpatterns = [
    path(
        r"/<uuid:uid>/tags/<uuid:tag_uid>",
        products.PrivateProductTagDetail.as_view(),
        name="we.product_tag-detail",
    ),
    path(
        "/<uuid:uid>/images/<uuid:image_uid>/cover-image",
        products.PrivateProductCoverImageDetail.as_view(),
        name="we.product_cover_image-detail",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:image_uid>",
        products.PrivateProductImageDetail.as_view(),
        name="we.product_image-detail",
    ),
    path(
        r"/<uuid:uid>/images",
        products.PrivateProductImageList.as_view(),
        name="we.product_image-list",
    ),
    path(
        r"/<uuid:uid>/files/<uuid:file_uid>",
        products.PrivateProductFileDetail.as_view(),
        name="we.product_file-detail",
    ),
    path(
        r"/<uuid:uid>/files",
        products.PrivateProductFileList.as_view(),
        name="we.product_file-list",
    ),
    # path(
    #     r"/ads/<uuid:uid>",
    #     products.PrivateProductAdsDetail.as_view(),
    #     name="we.product-ads-detail",
    # ),
    # path(r"/ads", products.PrivateProductAdsList.as_view(), name="we.product-ads"),
    path(
        r"/<uuid:uid>",
        products.PrivateProductDetail.as_view(),
        name="we.product-detail",
    ),
    path(r"", products.PrivateProductList.as_view(), name="we.product-list"),
]
