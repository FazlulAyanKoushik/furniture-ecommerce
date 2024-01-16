from django.urls import path

from ..views.materials import PrivateMaterialDetail, PrivateMaterialList

urlpatterns = [
    path(r"/<uuid:uid>", PrivateMaterialDetail.as_view(), name="we.material-detail"),
    path(r"", PrivateMaterialList.as_view(), name="we.material-list"),
]
