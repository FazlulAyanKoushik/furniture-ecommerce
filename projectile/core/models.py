import logging
import uuid
import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _


from autoslug import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField

from common.lists import COUNTRIES
from common.models import BaseModelWithUID
from common.fields import TimestampImageField

from accountio.choices import OrganizationUserStatus

from .choices import UserEmailStatus, UserGender, UserStatus, UserObjective
from .managers import CustomUserManager, UserEmailQuerySet
from .signals import (
    post_save_user,
    post_delete_user,
)
from .utils import (
    get_user_slug,
    get_user_media_path_prefix,
)

from versatileimagefield.fields import VersatileImageField

logger = logging.getLogger(__name__)


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(unique=True, db_index=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(
        max_length=2, choices=COUNTRIES, default="se", db_index=True
    )
    language = models.CharField(max_length=2, default="en")
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    has_newsletter = models.BooleanField(default=True)
    has_weekletter = models.BooleanField(default=True)
    enable_email = models.BooleanField(default=True)
    enable_push = models.BooleanField(default=True)
    headline = models.CharField(max_length=50, blank=True)
    summary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from=get_user_slug, unique=True, db_index=True)
    avatar = VersatileImageField(
        "Avatar",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    hero = VersatileImageField(
        "Hero",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        db_index=True,
        default=UserStatus.DRAFT,
    )
    gender = models.CharField(
        max_length=20, blank=True, null=True, choices=UserGender.choices, db_index=True
    )
    objective = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=UserObjective.choices,
        db_index=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)

    # Other links
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"ID: {self.id}, Email: {self.email}"

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def activate(self):
        self.is_active = True
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()
        UserEmail.objects.create(
            user=self, email=self.email, status=UserEmailStatus.ACTIVE, is_primary=True
        )

    def get_organization_user(self):
        queryset = self.profiles.select_related("organization", "user").filter(
            is_default=True
        )
        if queryset.exists():
            return queryset.order_by("-updated_at").first()
        return queryset.filter().order_by("-updated_at").first()

    def get_organization(self):
        organization_user = self.get_organization_user()
        if organization_user:
            return self.get_organization_user().organization
        return None

    def get_profiles(self):
        # Return all OrganizationUser instances connected to core.User
        statuses = [OrganizationUserStatus.PENDING, OrganizationUserStatus.ACTIVE]
        return self.profiles.select_related("user").filter(status__in=statuses)

    # Change status field
    def set_status_paused(self):
        self.status = UserStatus.PAUSED
        self.save_dirty_fields()

    def set_status_unpaused(self):
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()

    def set_status_removed(self):
        # Change User model
        self.status = UserStatus.REMOVED
        hashed_email = hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()
        self.email = f"{hashed_email}@none.supplers.com"
        self.username = f"{hashed_email}@none.supplers.com"
        self.last_name = self.last_name[0]
        self.avatar = None
        self.hero = None
        # TODO: Delete images related to user from S3.
        self.is_active = False
        self.set_unusable_password()
        self.save_dirty_fields()
        # Change related data
        self.get_profiles().update(status=OrganizationUserStatus.REMOVED)


class UserEmail(BaseModelWithUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=UserEmailStatus.choices,
        db_index=True,
        default=UserEmailStatus.PENDING,
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(default="127.0.0.1")

    objects = UserEmailQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "User Emails"
        ordering = ("created_at",)
        unique_together = ("user", "email")

    def __str__(self):
        return f"ID: {self.id}, User: {self.user}, Email: {self.email}"

    def make_primary(self):
        self.is_primary = True
        self.save(update_fields=["is_primary"])

    def consume_token(self):
        self.status = UserEmailStatus.ACTIVE
        self.token = None
        self.save(update_fields=["status", "token"])

    def is_status_active(self):
        return self.status == UserEmailStatus.ACTIVE

    def save(self, *args, **kwargs):
        if self.is_primary:
            self.user.useremail_set.filter(is_primary=True).exclude(id=self.id).update(
                is_primary=False
            )
        super(UserEmail, self).save(*args, **kwargs)


# Signals
post_save.connect(post_save_user, sender=User)
post_delete.connect(post_delete_user, sender=User)
