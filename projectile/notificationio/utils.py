from accountio.models import Organization

from . import models
from .choices import NotificationKind
from .helpers import NotificationHelper


def get_notification_slug(instance):
    return f"{instance.organization.name}"


def create_notification(organization, instance, targets, message, notification_kind):
    notification_map = {
        NotificationKind.NEW_PRODUCT: (
            NotificationHelper.create_new_product,
            "new_product",
        ),
        NotificationKind.NEW_PROJECT: (
            NotificationHelper.create_new_project,
            "new_project",
        ),
        NotificationKind.NEW_BRAND: (
            NotificationHelper.create_new_brand,
            "new_brand",
        ),
        NotificationKind.INVITE_REQUEST: (
            NotificationHelper.create_organization_invite,
            "invite_request",
        ),
        NotificationKind.INVITE_ACCEPTED: (
            NotificationHelper.create_organization_invite,
            "invite_accepted",
        ),
        NotificationKind.INVITE_REJECTED: (
            NotificationHelper.create_organization_invite,
            "invite_rejected",
        ),
        NotificationKind.GROUP_INVITE_REQUEST: (
            NotificationHelper.create_group_invite,
            "group_invite_request",
        ),
        NotificationKind.GROUP_INVITE_ACCEPTED: (
            NotificationHelper.create_group_invite,
            "group_invite_accepted",
        ),
        NotificationKind.GROUP_INVITE_REJECTED: (
            NotificationHelper.create_group_invite,
            "group_invite_rejected",
        ),
        NotificationKind.NEWS_POST: (NotificationHelper.create_new_post, "news_post"),
        NotificationKind.EVENT_POST: (NotificationHelper.create_new_post, "event_post"),
        NotificationKind.PRODUCT_PRICING: (
            NotificationHelper.create_new_product_discount,
            "product_pricing",
        ),
        NotificationKind.FILE: (NotificationHelper.create_file_item_access, "file"),
    }

    notification_settings = models.NotificationSettings.objects.filter(
        organization__in=targets
    ).values(
        "organization",
        "email_notifications",
        "turn_off_notifications",
        *set(attr for _, attr in notification_map.values()),
    )

    for setting in notification_settings:
        target = setting["organization"]
        attr = notification_map.get(notification_kind, (None, None))[1]
        if not setting["turn_off_notifications"] and setting["email_notifications"]:
            NotificationHelper.send_email_notification(target, message, instance, notification_kind)
        if not setting["turn_off_notifications"] and attr and setting[attr]:
            notification_function = notification_map.get(
                notification_kind, (None, None)
            )[0]
            if notification_function is not None:
                try:
                    target_instance = Organization.objects.get(pk=target)
                    notification_function(
                        organization,
                        instance,
                        target_instance,
                        message,
                        notification_kind,
                    )
                except Organization.DoesNotExist:
                    pass
