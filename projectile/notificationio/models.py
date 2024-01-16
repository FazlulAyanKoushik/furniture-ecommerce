from django.conf import settings
from django.db import models

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from . import utils

from .choices import ModelKind, NotificationKind, NotificationSettingsKind

from .managers import NotificationManager


class Notification(BaseModelWithUID):
    organization = models.ForeignKey(
        "accountio.Organization",
        on_delete=models.CASCADE,
        related_name="organization_set",
    )
    slug = AutoSlugField(
        populate_from=utils.get_notification_slug, unique=True, db_index=True
    )
    target = models.ForeignKey(
        "accountio.Organization",
        on_delete=models.SET_NULL,
        null=True,
        related_name="receivers_set",
    )
    kind = models.CharField(max_length=30, choices=NotificationKind.choices)
    message = models.CharField(max_length=255)
    is_unread = models.BooleanField(default=True)

    # Related Foreign keys
    product = models.ForeignKey(
        "catalogio.Product", on_delete=models.CASCADE, null=True, blank=True
    )
    project = models.ForeignKey(
        "collabio.Project", on_delete=models.CASCADE, null=True, blank=True
    )
    organization_invite = models.ForeignKey(
        "invitio.OrganizationInvite", on_delete=models.CASCADE, null=True, blank=True
    )
    member = models.ForeignKey(
        "gruppio.Member", on_delete=models.CASCADE, null=True, blank=True
    )
    post = models.ForeignKey(
        "newsdeskio.NewsdeskPost", on_delete=models.CASCADE, null=True, blank=True
    )
    discount = models.ForeignKey(
        "catalogio.ProductDiscount", on_delete=models.CASCADE, blank=True, null=True
    )
    file = models.ForeignKey(
        "fileroomio.FileItemAccess", on_delete=models.CASCADE, blank=True, null=True
    )
    brand = models.ForeignKey(
        "catalogio.ProductBrand", on_delete=models.CASCADE, blank=True, null=True
    )
    service = models.ForeignKey(
        "catalogio.Service", on_delete=models.CASCADE, blank=True, null=True
    )
    model_kind = models.CharField(
        max_length=20, choices=ModelKind.choices, db_index=True
    )

    objects = NotificationManager.as_manager()

    def __str__(self):
        try:
            if self.model_kind == ModelKind.PRODUCT:
                return f"Product: {self.product.title}"
            if self.model_kind == ModelKind.PROJECT:
                return f"Project: {self.project.title}"
            if self.model_kind == ModelKind.ORGANIZATION_INVITE:
                return f"Organization: {self.organization_invite.organization.name}, Target: {self.target.name}"
            if self.model_kind == ModelKind.MEMBER:
                return f"Member: {self.member.user.get_name()}"
            if self.model_kind == ModelKind.NEWS_DESK_POST:
                return f"Post Title: {self.post.title}, Kind: {self.post.kind}"
            if self.model_kind == ModelKind.PRODUCT_DISCOUNT:
                return f"Product Discount: {self.discount.category}"
            if self.model_kind == ModelKind.FILE_ITEM_ACCESS:
                return f"File Item Access: {self.file.kind}"
            if self.model_kind == ModelKind.BRAND:
                return f"Brand: {self.brand.title}"
            if self.model_kind == ModelKind.SERVICE:
                return f"Service: {self.service.title}"

        except AttributeError:
            pass

        return None

    class Meta:
        ordering = ["-created_at"]

    def mark_as_read(self):
        self.is_unread = False
        self.save_dirty_fields()


class NotificationSettings(BaseModelWithUID):
    organization = models.OneToOneField(
        "accountio.Organization", on_delete=models.CASCADE, blank=True, null=True
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    turn_off_notifications = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    new_brand = models.BooleanField(default=True)
    new_product = models.BooleanField(default=True)
    new_project = models.BooleanField(default=True)
    new_service = models.BooleanField(default=True)
    invite_request = models.BooleanField(default=True)
    invite_accepted = models.BooleanField(default=True)
    invite_rejected = models.BooleanField(default=True)
    group_invite_request = models.BooleanField(default=True)
    group_invite_accepted = models.BooleanField(default=True)
    group_invite_rejected = models.BooleanField(default=True)
    news_post = models.BooleanField(default=True)
    event_post = models.BooleanField(default=True)
    post_reply = models.BooleanField(default=True)
    post_like = models.BooleanField(default=True)
    product_pricing = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    file = models.BooleanField(default=True)
    kind = models.CharField(
        max_length=20, choices=NotificationSettingsKind.choices, db_index=True
    )

    class Meta:
        verbose_name_plural = "Notification Settings"

    def __str__(self):
        return f"Organization: {self.organization}"
