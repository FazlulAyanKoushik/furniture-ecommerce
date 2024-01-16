from django.db.models.signals import post_save
from django.dispatch import receiver

# from firebase_admin import db

from accountio.models import Organization

from catalogio.models import Product, ProductDiscount, ProductBrand, Service

from collabio.models import Project

from fileroomio.choices import FileItemAccessKind
from fileroomio.models import FileItemAccess

from gruppio.choices import MemberStatus
from gruppio.models import Member

from invitio.choices import OrganizationInviteResponse
from invitio.models import OrganizationInvite

from newsdeskio.choices import NewsdeskPostKind
from newsdeskio.models import NewsdeskPost

from notificationio.models import NotificationSettings
from notificationio.choices import NotificationSettingsKind

from .choices import NotificationKind
from . import utils
@receiver(post_save, sender=Product)
def create_notification_for_product(sender, instance, created, **kwargs):
    if created:
        message = f"A new product has been added: {instance.title}"
        organization = instance.organization
        targets = organization.get_descendants()
        utils.create_notification(
            organization, instance, targets, message, NotificationKind.NEW_PRODUCT
        )


@receiver(post_save, sender=Project)
def create_notification_for_project(sender, instance, created, **kwargs):
    if created:
        message = f"A new project has been added: {instance.title}"
        organization = instance.organization
        targets = organization.get_descendants()
        utils.create_notification(
            organization, instance, targets, message, NotificationKind.NEW_PROJECT
        )

@receiver(post_save, sender=ProductBrand)
def create_notification_for_brand(sender, instance, created, **kwargs):
    if created:
        message = f"A new brand has been created: {instance.title}"
        organization = instance.organization
        targets = organization.get_descendants()
        utils.create_notification(
            organization, instance, targets, message, NotificationKind.NEW_BRAND
        )


@receiver(post_save, sender=NewsdeskPost)
def create_notification_for_news_event_post(sender, instance, created, **kwargs):
    if created:
        organization = instance.organization
        targets = organization.get_descendants()
        kind = ""
        message = ""

        if instance.kind == NewsdeskPostKind.NEWS:
            message = f"A new news has been posted: {instance.title}"
            kind = NotificationKind.NEWS_POST
        elif instance.kind == NewsdeskPostKind.EVENT:
            message = f"A new event has been posted: {instance.title}"
            kind = NotificationKind.EVENT_POST

        utils.create_notification(organization, instance, targets, message, kind)


@receiver(post_save, sender=OrganizationInvite)
def create_notification_for_organization_invite(sender, instance, **kwargs):
    organization = instance.organization
    target = instance.target
    kind = ""
    message = ""

    if instance.response == OrganizationInviteResponse.PENDING:
        message = (
            f"You have received a new invitation from: {instance.organization.name}"
        )
        kind = NotificationKind.INVITE_REQUEST

    elif instance.response == OrganizationInviteResponse.DECLINED:
        message = f"Your request has been rejected by: {instance.organization.name}"
        kind = NotificationKind.INVITE_REJECTED
        organization = instance.target
        target = instance.organization

    elif instance.response == OrganizationInviteResponse.ACCEPTED:
        message = f"Your request has been accepted by: {instance.target.name}"
        kind = NotificationKind.INVITE_ACCEPTED
        organization = instance.target
        target = instance.organization

    utils.create_notification(organization, instance, [target], message, kind)


@receiver(post_save, sender=Member)
def create_notification_for_group_invite(sender, instance, **kwargs):
    organization = instance.group.organization
    target = instance.user.get_organization()

    kind = ""
    message = ""

    if instance.status == MemberStatus.PENDING:
        message = f"You have received a new group invite from: {instance.group.name}"
        kind = NotificationKind.GROUP_INVITE_REQUEST

    elif instance.status == MemberStatus.USER_ACCEPTED:
        message = f"Your request has been accepted."
        kind = NotificationKind.GROUP_INVITE_ACCEPTED
        organization = target
        target = organization

    elif instance.status == MemberStatus.USER_REJECTED:
        message = f"Your request has been rejected by: {target.name}"
        kind = NotificationKind.GROUP_INVITE_REJECTED
        organization = target
        target = organization

    utils.create_notification(organization, instance, [target], message, kind)


@receiver(post_save, sender=ProductDiscount)
def create_notification_for_product_discount(sender, instance, created, **kwargs):
    if created:
        organization = instance.organization
        kind = NotificationKind.PRODUCT_PRICING
        target = instance.target
        message = f"A special discount has been added for you on {instance.category}"
        utils.create_notification(organization, instance, [target], message, kind)


@receiver(post_save, sender=FileItemAccess)
def create_notification_for_file_item_access(sender, instance, **kwargs):
    organization = instance.fileitem.organization
    kind = NotificationKind.FILE
    message = f"A new file has been added by {organization.name}"

    if instance.kind == FileItemAccessKind.PARTNER:
        target = instance.partner

    elif instance.kind == FileItemAccessKind.USER:
        target = instance.user.get_organization()

    utils.create_notification(organization, instance, [target], message, kind)


@receiver(post_save, sender=Organization)
def create_notification_setting(sender, instance, created, **kwargs):
    if created:
        NotificationSettings.objects.create(
            organization=instance, kind=NotificationSettingsKind.ORGANIZATION
        )


# def update_firebase_notification_count(instance):
#     organization = instance.target
#     url = f"/notifications/{organization.slug}/"
#     ref = db.reference(url)
#     ref.push(
#         {
#             "count": organization.target_set.filter(is_read=False).count(),
#             "timestamp": {".sv": "timestamp"},
#         }
#     )


# def post_save_notification(sender, instance, created, *args, **kwargs):
#     update_firebase_notification_count(instance)


# def post_delete_notification(sender, instance, *args, **kwargs):
#     update_firebase_notification_count(instance)
