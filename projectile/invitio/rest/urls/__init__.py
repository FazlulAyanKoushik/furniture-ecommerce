from django.urls import include, path

from ..views.profiles import ProfileDetail

urlpatterns = [
    path(
        "/profiles/<uuid:token>",
        ProfileDetail.as_view(),
        name="invites.profile-detail",
    ),
]
