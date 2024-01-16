from django.urls import path

from ..views import mediaroom

from ..views.groups import (
    PrivateGroupDetail,
    PrivateGroupList,
    PrivateMemberDetail,
    PrivateMemberList,
    PrivateGroupFileList,
    PrivateGroupFileDetail,
    PrivateGroupImageList,
    PrivateGroupImageDetail,
)

urlpatterns = [
    path(
        r"/<uuid:uid>",
        PrivateGroupDetail.as_view(),
        name="we.group-detail",
    ),
    path(
        r"/<uuid:group_uid>/members",
        PrivateMemberList.as_view(),
        name="we.group.member-list",
    ),
    path(
        r"/<uuid:group_uid>/members/<uuid:uid>",
        PrivateMemberDetail.as_view(),
        name="we.group.member-detail",
    ),
    path(
        r"/<uuid:uid>/files/<uuid:group_uid>",
        PrivateGroupFileDetail.as_view(),
        name="we.group_file-detail",
    ),
    path(
        r"/<uuid:uid>/files",
        PrivateGroupFileList.as_view(),
        name="we.group_file-list",
    ),
    path(
        r"",
        PrivateGroupList.as_view(),
        name="we.group-list",
    ),
    path(
        r"/<uuid:uid>/images",
        PrivateGroupImageList.as_view(),
        name="we.group_image-list",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:group_uid>",
        PrivateGroupImageDetail.as_view(),
        name="we.group_image-detail",
    ),
]
