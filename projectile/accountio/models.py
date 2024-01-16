import logging
import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField

from catalogio.choices import ServiceStatus
from catalogio.models import Service
from common.lists import COUNTRIES
from common.models import BaseModelWithUID

from paymentio.choices import SubscriptionSessionStatus, SubscriptionTransactionStatus

from .choices import (
    OrganizationKind,
    OrganizationUserRole,
    OrganizationUserStatus,
    OrganizationSize,
    OrganizationStatus,
)

from .managers import (
    OrganizationQuerySet,
    OrganizationUserQuerySet,
)
from .signals import (
    post_save_descendant,
    post_save_organization,
    post_save_organization_user,
    post_delete_organization,
)
from .utils import (
    get_organization_slug,
    get_organization_media_path_prefix,
    get_customer_service_slug,
)

logger = logging.getLogger(__name__)


class Organization(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from=get_organization_slug, unique=True, db_index=True
    )
    registration_no = models.CharField(max_length=50, blank=True)
    vat_no = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=50, blank=True)
    postal_area = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(
        max_length=2, choices=COUNTRIES, default="se", db_index=True
    )
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    county = models.CharField(max_length=50, blank=True)
    segment = models.CharField(max_length=50, blank=True)
    source = models.CharField(max_length=50, blank=True)
    # JSON fields
    scraped = models.JSONField(default=dict, null=False, blank=True)
    categories = models.JSONField(default=list, null=False, blank=True)
    # Links to other external urls
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    size = models.CharField(
        max_length=20, choices=OrganizationSize.choices, default=OrganizationSize.ZERO
    )
    summary = models.TextField(blank=True, help_text="Short summary about company.")
    description = models.TextField(
        blank=True, help_text="Longer description about company."
    )
    kind = models.CharField(
        max_length=20,
        choices=OrganizationKind.choices,
        db_index=True,
        default=OrganizationKind.UNKNOWN,
    )
    status = models.CharField(
        max_length=20,
        choices=OrganizationStatus.choices,
        db_index=True,
        default=OrganizationStatus.DRAFT,
    )
    parents = models.ManyToManyField(
        "self", through="Descendant", through_fields=("child", "parent")
    )
    # Image Fields
    avatar = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    hero = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    logo_wide = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    image = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    note = models.TextField(blank=True)
    # Track changes in model
    history = HistoricalRecords()
    # Use custom managers
    objects = OrganizationQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)
        unique_together = (("registration_no", "country"),)

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Country: {self.country}"

    def get_name(self):
        return self.display_name or self.name

    def get_descendants(self):
        ids = self.descendant_set.filter().values_list("child_id", flat=True).distinct()
        return Organization.objects.get_status_fair().filter(id__in=ids)

    def has_partner_services(self):
        ids = self.descendant_set.filter().values_list("child_id", flat=True).distinct()
        return Service.objects.filter(
            organization__id__in=ids, status=ServiceStatus.ACTIVE
        ).exists()

    def get_users(self):
        statuses = [OrganizationUserStatus.PENDING, OrganizationUserStatus.ACTIVE]
        roles = [
            OrganizationUserRole.STAFF,
            OrganizationUserRole.ADMIN,
            OrganizationUserRole.OWNER,
        ]
        return self.organizationuser_set.filter(role__in=roles, status__in=statuses)

    def add_owner(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.OWNER,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_admin(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.ADMIN,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_staff(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.STAFF,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_initiator(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.INITIATOR,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def is_kind_supplier(self):
        return self.kind == OrganizationKind.SUPPLIER

    def is_kind_retailer(self):
        return self.kind == OrganizationKind.RETAILER

    def is_kind_architect(self):
        return self.kind == OrganizationKind.ARCHITECT

    def set_slug(self):
        self.slug = get_organization_slug(self)
        logger.debug(self.slug)
        self.save_dirty_fields()

    def is_status_draft(self):
        return self.status == OrganizationStatus.DRAFT

    def is_status_placeholder(self):
        return self.status == OrganizationStatus.PLACEHOLDER

    def is_status_pending(self):
        return self.status == OrganizationStatus.PENDING

    def is_status_active(self):
        return self.status == OrganizationStatus.ACTIVE

    def set_status_pending(self):
        self.status = OrganizationStatus.PENDING
        self.save_dirty_fields()

    def set_status_active(self):
        self.status = OrganizationStatus.ACTIVE
        self.save_dirty_fields()

    def set_status_removed(self):
        # Soft delete because there might be linked data
        self.status = OrganizationStatus.REMOVED
        self.save(update_fields=["status", "updated_at"])
        self.organizationuser_set.filter().update(status=OrganizationUserStatus.REMOVED)

    def has_pro_subscription(self):
        return self.subscriptionsession_set.filter(
            status=SubscriptionSessionStatus.ACTIVE,
            stop_date__isnull=True,
            start_date__lte=timezone.now(),
            subscriptiontransaction__status=SubscriptionTransactionStatus.SUCCEEDED,
        ).exists()


class OrganizationUser(BaseModelWithUID):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )
    role = models.CharField(max_length=20, choices=OrganizationUserRole.choices)
    designation = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OrganizationUserStatus.choices,
        db_index=True,
        default=OrganizationUserStatus.PENDING,
    )
    is_default = models.BooleanField(default=False)
    referrer = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    reminded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    # Custom managers use
    objects = OrganizationUserQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Organization Users"
        ordering = ("created_at",)
        unique_together = ("organization", "user")

    def __str__(self):
        return f"ID: {self.id}, Org: {self.organization}, User: {self.user}, Role: {self.role}, Status: {self.status}"

    def set_role_staff(self):
        self.role = OrganizationUserRole.STAFF
        self.save_dirty_fields()

    def set_role_owner(self):
        self.role = OrganizationUserRole.OWNER
        self.save_dirty_fields()

    def set_status_pending(self):
        self.status = OrganizationUserStatus.PENDING
        self.save_dirty_fields()

    def set_status_active(self):
        self.status = OrganizationUserStatus.ACTIVE
        self.save_dirty_fields()

    def set_status_hidden(self):
        self.status = OrganizationUserStatus.HIDDEN
        self.save_dirty_fields()

    def set_status_removed(self):
        self.status = OrganizationUserStatus.REMOVED
        self.save_dirty_fields()

    def select(self):
        self.is_default = True
        # Do not use .save_dirty_fields here
        # because it will not call the side effects
        # necessary for this to work
        self.save()

    def accept(self):
        self.status = OrganizationUserStatus.ACTIVE
        fields = ["status"]
        if not self.user.users.filter(user=self.user, is_default=True).exists():
            fields.append("is_default")
            self.is_default = True
        self.save()

    def reject(self):
        self.status = OrganizationUserStatus.REJECTED
        self.save_dirty_fields()

    def remind(self):
        now = timezone.now()
        self.reminded_at = now
        self.save_dirty_fields()

    def save(self, *args, **kwargs):
        if self.is_default:
            OrganizationUser.objects.filter(user=self.user, is_default=True).update(
                is_default=False
            )
        super(OrganizationUser, self).save(*args, **kwargs)


class Descendant(BaseModelWithUID):
    """
    To keep track of <Organization>s and their sub <Organisation>s relationships.
    An <Organization> can have 0 or n sub <Organisation>s.
    """

    parent = models.ForeignKey(
        Organization, related_name="descendant_set", on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        Organization, related_name="parent_set", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            "parent",
            "child",
        )
        unique_together = (
            "parent",
            "child",
        )

    def __str__(self):
        return f"Child: {self.child} of Parent: {self.parent}"


post_save.connect(post_save_organization, sender=Organization)
post_delete.connect(post_delete_organization, sender=Organization)
post_save.connect(post_save_organization_user, sender=OrganizationUser)
post_save.connect(post_save_descendant, sender=Descendant)