from django.urls import path

from ..views import collections

urlpatterns = [
    path(
        "",
        collections.PrivateOrganizationCollection.as_view(),
        name="collection.collection-list",
    ),
    path(
        "/<uuid:uid>",
        collections.PrivateOrganizationCollectionDetail.as_view(),
        name="collection.collection-detail",
    ),
    path(
        "/<uuid:uid>/products",
        collections.PrivateCollectionProductList.as_view(),
        name="collection.products",
    ),
]
