from django.urls import path

from weapi.rest.views.ads import (
    PrivateOrganizationAdFeatureList,
    PrivateOrganizationAdList,
    PrivateOrganizationAdDetail,
    PrivateProductAdList,
    PrivateProductAdDetail,
    PrivateProjectAdList,
    PrivateProjectAdDetail,
)


urlpatterns = [
    path(
        r"/organizations/<uuid:uid>",
        PrivateOrganizationAdDetail.as_view(),
        name="we.ad-organization-detail",
    ),
    path(
        r"/organizations",
        PrivateOrganizationAdList.as_view(),
        name="we.ad-organization-list",
    ),
    path(
        r"/products/<uuid:uid>",
        PrivateProductAdDetail.as_view(),
        name="we.product-ad-detail",
    ),
    path(r"/products", PrivateProductAdList.as_view(), name="we.product-ad-list"),
    path(
        r"/projects/<uuid:uid>",
        PrivateProjectAdDetail.as_view(),
        name="we.ad-project-detail",
    ),
    path(r"/projects", PrivateProjectAdList.as_view(), name="we.ad-project-list"),
    path(
        r"/features",
        PrivateOrganizationAdFeatureList.as_view(),
        name="we.ad-feature-list",
    ),
]
