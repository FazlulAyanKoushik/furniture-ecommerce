from django.urls import path

from ..views.organizations import SearchOrganizationList
from ..views.organizations_xlsx_file import OrganizationListExcelView
from ..views.products import GlobalProductSearchList

urlpatterns = [
    path(
        r"/organizations", SearchOrganizationList.as_view(), name="search.organizations"
    ),
    path(
        r"/organizations/download-excel",
        OrganizationListExcelView.as_view(),
        name="organization-list-excel",
    ),
    path(r"/products", GlobalProductSearchList.as_view(), name="search.products"),
]
