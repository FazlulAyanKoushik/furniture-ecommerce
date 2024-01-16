from django.urls import path

from ..views.brands import (
    PrivateOrganizationProductBrandList,
    PrivateOrganizationProductBrandDetail,
)

urlpatterns = [
    path(
        r"",
        PrivateOrganizationProductBrandList.as_view(),
        name="loggedin.user.organization-product-brand",
    ),
    path(
        r"/<uuid:uid>",
        PrivateOrganizationProductBrandDetail.as_view(),
        name="loggedin.user.organization.product-brand-detail",
    ),
]
