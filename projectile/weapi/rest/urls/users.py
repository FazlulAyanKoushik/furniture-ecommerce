from django.urls import path

from weapi.rest.views.users import (
    PrivateOrganizationUserList,
    PrivateOrganizationUserDetail,
    PrivateOrganizationUserSetPassword,
)

urlpatterns = [
    path(
        r"/invite/<slug:token>",
        PrivateOrganizationUserSetPassword.as_view(),
        name="we.invited-user-set-password",
    ),
    path(
        r"/<uuid:uid>",
        PrivateOrganizationUserDetail.as_view(),
        name="we.user-detail",
    ),
    path(
        r"",
        PrivateOrganizationUserList.as_view(),
        name="we.user-list",
    ),
]
