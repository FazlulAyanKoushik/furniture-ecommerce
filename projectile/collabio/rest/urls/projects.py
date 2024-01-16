from django.urls import path

from ..views.projects import (
    GlobalProjectDetail,
    GlobalProjectDetailImageList,
    GlobalProjectList,
)

urlpatterns = [
    path(
        r"/<slug:project_slug>",
        GlobalProjectDetail.as_view(),
        name="public.project-detail",
    ),
    path(
        r"/<slug:project_slug>/images",
        GlobalProjectDetailImageList.as_view(),
        name="public.project-detail-image-list",
    ),
    path(r"", GlobalProjectList.as_view(), name="public.project-list"),
]
