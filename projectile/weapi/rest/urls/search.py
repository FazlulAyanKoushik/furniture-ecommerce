from django.urls import path

from ..views.search import PrivateOrganizationSearchList


urlpatterns = [
    path(
        r"/partners",
        PrivateOrganizationSearchList.as_view(),
        name="we.search.partner-list",
    ),
]
