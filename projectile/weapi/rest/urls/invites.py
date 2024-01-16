from django.urls import path
from ..views import invites

urlpatterns = [
    path(
        r"/outgoing",
        invites.PrivateOutgoingInviteList.as_view(),
        name="we.invites.outgoing-list",
    ),
    path(
        r"/incoming/<slug:token>",
        invites.PrivateInviteResponseDetail.as_view(),
        name="we.invites.response-detail",
    ),
    path(
        r"/incoming",
        invites.PrivateIncomingInviteList.as_view(),
        name="we.invites.incoming-list",
    ),
]
