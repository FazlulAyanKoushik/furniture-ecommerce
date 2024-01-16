from django.urls import path

from ..views.notifications import PrivateNotificationSettings


urlpatterns = [
    path(
        r"",
        PrivateNotificationSettings.as_view(),
        name="we-notification-settings",
    ),
]
