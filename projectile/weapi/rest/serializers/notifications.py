from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from notificationio.models import NotificationSettings


class PrivateNotificationSettingsSerializer(serializers.ModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = NotificationSettings
        fields = [
            "uid",
            "organization",
            "email_notifications",
            "turn_off_notifications",
            "new_brand",
            "new_service",
            "new_product",
            "new_project",
            "invite_request",
            "invite_accepted",
            "invite_rejected",
            "group_invite_request",
            "group_invite_accepted",
            "group_invite_rejected",
            "news_post",
            "event_post",
            "post_reply",
            "post_like",
            "product_pricing",
            "push_notifications",
            "file",
        ]
        read_only_fields = ["uid", "organization"]
