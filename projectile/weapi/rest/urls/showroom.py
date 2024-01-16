from django.urls import path

from ..views.showroom import (
    PrivateOrganizationShowroomDetail,
    PrivateOrganizationShowroomList,
    PrivateShowRoomImageList,
    PrivateShowRoomImageDetail,
    PrivateShowRoomCoverImageDetail
)

urlpatterns = [
    path(
    r"/<uuid:uid>/images/<uuid:image_uid>/cover-image",
    PrivateShowRoomCoverImageDetail.as_view(),
    name="we.showroom-cover-image-change",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:image_uid>",
        PrivateShowRoomImageDetail.as_view(),
        name="we.showroom-image-detail",
    ),
    path(
        r"/<uuid:uid>/images",
        PrivateShowRoomImageList.as_view(),
        name="we.showroom-image-list",
    ),
    path(
        r"/<uuid:uid>",
        PrivateOrganizationShowroomDetail.as_view(),
        name="we.showroom-detail",
    ),
    path(r"", PrivateOrganizationShowroomList.as_view(), name="we.showroom-list"),
    path(
        "/<uuid:uid>/images/<uuid:image_uid>/cover-image",
        PrivateShowRoomImageDetail.as_view(),
        name="we.showroom_cover_image-detail",
    ),

    
]
