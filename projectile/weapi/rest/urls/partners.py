from django.urls import path
from weapi.rest.views.partners import (
    PrivateBulkCreatePartners,
    PrivateOrganizationPartnersDetail,
    PrivateOrganizationPartnersList,
    PrivateOrganizationPartnersDiscountList,
    PrivateOrganizationPartnersDiscountDetail,
    PrivateOrganizationPartnersFileList,
    PrivateOrganizationPartnerUserList,
    PrivatePartnersDiscountList,    
)

urlpatterns = [
    path(
        r"",
        PrivateOrganizationPartnersList.as_view(),
        name="we.partners-list",
    ),
    path(
        r"/discounts",
        PrivatePartnersDiscountList.as_view(),
        name="we.partners-discount-list",
    ),
    path(
        r"/<uuid:uid>",
        PrivateOrganizationPartnersDetail.as_view(),
        name="we.partners-detail",
    ),
    path(
        r"/<uuid:uid>/users",
        PrivateOrganizationPartnerUserList.as_view(),
        name="we.partner-user-list",
    ),    
    path(
        r"/create/file",
        PrivateBulkCreatePartners.as_view(),
        name="we.partners-file",
    ),
    path(
        r"/<uuid:uid>/discounts",
        PrivateOrganizationPartnersDiscountList.as_view(),
        name="we.partners-detail-discount-list",
    ),
    path(
        r"/<uuid:uid>/discounts/<uuid:discount_uid>",
        PrivateOrganizationPartnersDiscountDetail.as_view(),
        name="we.partners-detail-discount-detail",
    ),
    path(
        r"/<uuid:uid>/files",
        PrivateOrganizationPartnersFileList.as_view(),
        name="we.partners-detail-file-list",
    ),
]
