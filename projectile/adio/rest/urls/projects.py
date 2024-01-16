from django.urls import path

from ..views.projects import GlobalProjectAdList, GlobalProjectAdDetail

urlpatterns = [
    path(
        r"/<slug:slug>",
        GlobalProjectAdDetail.as_view(),
        name="global.ad-project-detail",
    ),
    path(r"", GlobalProjectAdList.as_view(), name="global.ad-project-list"),
]
