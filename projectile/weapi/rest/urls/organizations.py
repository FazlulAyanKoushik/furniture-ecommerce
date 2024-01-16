from django.urls import path

from ..views.organizations import PrivateSelfOrganzationList

urlpatterns = [
    path(r"", PrivateSelfOrganzationList.as_view(), name="we.self.organizations-list"),
]
