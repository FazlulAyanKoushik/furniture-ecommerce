from django.urls import path

from populario.rest.views.organizations import (
    GlobalPopularOrganizationList,
    GlobalPopularOrganizationDetail,
)


urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalPopularOrganizationDetail.as_view(),
        name="global.popular-organization-detail",
    ),
    path(
        r"",
        GlobalPopularOrganizationList.as_view(),
        name="global.popular-organization-list",
    ),
]
