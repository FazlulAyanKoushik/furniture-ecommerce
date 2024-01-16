from django.urls import path

from weapi.rest.views.status import PrivateWeStatusDetail


urlpatterns = [
    path(
        r"",
        PrivateWeStatusDetail.as_view(),
        name="we.we-status-detail",
    ),
]
