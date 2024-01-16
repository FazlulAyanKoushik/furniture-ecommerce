from django.urls import path

from ..views.groups import (
    GlobalGroupList,
    GlobalGroupDetail,
    GlobalGroupAdminList,
    GlobalMemberList,
    GlobalMemberDetail,
)

urlpatterns = [
    path(r"/<slug:slug>", GlobalGroupDetail.as_view(), name="group.detail"),
    path(r"/<slug:slug>/admins", GlobalGroupAdminList.as_view(), name="admins.list"),
    path(r"/<slug:slug>/members", GlobalMemberList.as_view(), name="members.list"),
    path(
        r"/<slug:group_slug>/members/<uuid:uid>",
        GlobalMemberDetail.as_view(),
        name="members.detail",
    ),
    path(r"", GlobalGroupList.as_view(), name="group.list"),
]
