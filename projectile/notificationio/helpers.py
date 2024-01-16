from django.conf import settings

from common.tasks import send_email_async

from accountio.models import Organization

from notificationio.choices import NotificationKind

from . import models


class NotificationHelper:
    @staticmethod
    def create_new_product(organization, product, target, message, kind):
        return models.Notification.objects.create_new_product(
            organization, product, target, message, kind
        )

    @staticmethod
    def create_new_project(organization, project, target, message, kind):
        return models.Notification.objects.create_new_project(
            organization, project, target, message, kind
        )

    @staticmethod
    def create_new_brand(organization, brand, target, message, kind):
        return models.Notification.objects.create_new_brand(
            organization, brand, target, message, kind
        )

    @staticmethod
    def create_new_post(organization, newsdeskpost, target, message, kind):
        return models.Notification.objects.create_new_post(
            organization, newsdeskpost, target, message, kind
        )

    @staticmethod
    def create_organization_invite(
        organization, organization_invite, target, message, kind
    ):
        return models.Notification.objects.create_organization_invite(
            organization, organization_invite, target, message, kind
        )

    @staticmethod
    def create_group_invite(organization, member, target, message, kind):
        return models.Notification.objects.create_group_invite(
            organization, member, target, message, kind
        )

    @staticmethod
    def create_new_product_discount(organization, discount, target, message, kind):
        return models.Notification.objects.create_new_product_discount(
            organization, discount, target, message, kind
        )

    @staticmethod
    def create_file_item_access(organization, file, target, message, kind):
        return models.Notification.objects.create_file_item_access(
            organization, file, target, message, kind
        )

    @staticmethod
    def send_email_notification(target, message, instance, notification_kind):
        target_organization = Organization.objects.filter(id=target).first()
        users = target_organization.get_users()
        site_url = (
            "http://localhost:3000" if settings.DEBUG else "https://www.supplers.com"
        )
        if (
            notification_kind == NotificationKind.NEWS_POST
            or notification_kind == NotificationKind.EVENT_POST
        ):
            site_url = (
                f"{site_url}/partners/{instance.organization.slug}/news/{instance.slug}"
            )
        for user in users:
            context = {
                "name": user.user.get_name(),
                "message": message,
                "site_url": site_url,
            }
            template = "email/notification.html"
            email = user.user.email
            subject = message
            send_email_async(context, template, email, subject)
