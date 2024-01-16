from django.urls import path

from ..views.organizations import (
    GlobalOrganizationAdList,
    GlobalOrganizationAdDetail,
)


urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalOrganizationAdDetail.as_view(),
        name="global.ad-organization-detail",
    ),
    path(r"", GlobalOrganizationAdList.as_view(), name="global.ad-organization-list"),
]
