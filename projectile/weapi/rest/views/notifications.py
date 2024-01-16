from rest_framework.generics import (
    get_object_or_404,
    RetrieveUpdateAPIView,
)

from accountio.rest.permissions import IsOrganizationStaff

from notificationio.models import NotificationSettings

from ..serializers.notifications import PrivateNotificationSettingsSerializer


class PrivateNotificationSettings(RetrieveUpdateAPIView):
    serializer_class = PrivateNotificationSettingsSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        return get_object_or_404(
            NotificationSettings.objects.filter(),
            organization=self.request.user.get_organization(),
        )
