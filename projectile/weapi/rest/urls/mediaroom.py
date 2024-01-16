from django.urls import path

from ..views.mediaroom import (
    PrivateOrganizationImageDetail,
    PrivateOrganizationImageList,
)

urlpatterns = [
    path(
        r"/<uuid:uid>", PrivateOrganizationImageDetail.as_view(), name="we.image-detail"
    ),
    path(r"", PrivateOrganizationImageList.as_view(), name="we.image-list"),
]
