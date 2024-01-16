from django.urls import path

from weapi.rest.views import projects

urlpatterns = [
    path(
        r"/<uuid:project_uid>",
        projects.PrivateProjectDetailView.as_view(),
        name="we.projects-detail",
    ),
    path(
        r"/<uuid:project_uid>/participants",
        projects.PrivateProjectParticipantListView.as_view(),
        name="we.participants-list",
    ),
    path(
        r"/<uuid:project_uid>/participants/<uuid:participant_uid>",
        projects.PrivateProjectParticipantDetailView.as_view(),
        name="we.participants-detail",
    ),
    path(
        r"/<uuid:uid>/images",
        projects.PrivateProjectImageList.as_view(),
        name="we.project_image-list",
    ),
    path(
        r"/<uuid:uid>/files/<uuid:file_uid>",
        projects.PrivateProjectFileDetail.as_view(),
        name="we.project_file-detail",
    ),
    path(
        r"/<uuid:uid>/files",
        projects.PrivateProjectFileList.as_view(),
        name="we.project_file-list",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:image_uid>",
        projects.PrivateProjectImageDetail.as_view(),
        name="we.project_image-detail",
    ),
    path(
        r"/<uuid:uid>/images/<uuid:image_uid>/cover-image",
        projects.PrivateProjectCoverImageDetail.as_view(),
        name="we.project_cover_image-detail"
    ),
    path(
        r"",
        projects.PrivateProjectListView.as_view(),
        name="we.projects-list",
    ),
]
