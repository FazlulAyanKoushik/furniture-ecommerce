from django.urls import path

from populario.rest.views.projects import (
    GlobalPopularProjectList,
    GlobalPopularProjectDetail,
)


urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalPopularProjectDetail.as_view(),
        name="global.popular-project-detail",
    ),
    path(
        r"",
        GlobalPopularProjectList.as_view(),
        name="global.popular-project-list",
    ),
]
