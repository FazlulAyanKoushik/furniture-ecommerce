from django.core.management.base import BaseCommand

from accountio.models import Organization

from notificationio.choices import NotificationSettingsKind
from notificationio.models import NotificationSettings


class Command(BaseCommand):
    help = "Create missing notification settings for existing organizations"

    def handle(self, *args, **options):
        organizations = Organization.objects.filter(notificationsettings__isnull=True)

        notification_settings = [
            NotificationSettings(organization=organization, kind=NotificationSettingsKind.ORGANIZATION)
            for organization in organizations
        ]
        NotificationSettings.objects.bulk_create(notification_settings)

        self.stdout.write(
            self.style.SUCCESS(
                "Notification settings created for existing organizations"
            )
        )
