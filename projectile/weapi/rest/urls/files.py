from django.urls import path

from ..views.files import PrivateOrganizationFileList, PrivateOrganizationFileDetail

urlpatterns = [
    path(
        r"/<uuid:uid>", PrivateOrganizationFileDetail.as_view(), name="we.file-detail"
    ),
    path(r"", PrivateOrganizationFileList.as_view(), name="we.files-list"),
]
