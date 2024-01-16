from django.urls import path

from ..views import service

urlpatterns = [
    path(
        "/<uuid:uid>",
        service.PrivateServiceDetail.as_view(),
        name="we.service-detail",
    ),
    path("", service.PrivateServiceList.as_view(), name="we.service-list"),
]
