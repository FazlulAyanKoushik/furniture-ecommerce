import logging
import uuid

from django.apps import apps
from django.conf import settings
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

from autoslug import AutoSlugField

from common.fields import TimestampImageField
from common.lists import COUNTRIES
from common.models import BaseModelWithUID


from .choices import GroupKind, GroupStatus, MemberRole, MemberStatus
from .managers import GroupQuerySet, MemberQuerySet
from .signals import post_save_member, post_delete_member
from .utils import get_group_media_path_prefix

from versatileimagefield.fields import VersatileImageField


logger = logging.getLogger(__name__)


class Group(BaseModelWithUID):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    avatar = VersatileImageField(
        "Avatar",
        upload_to=get_group_media_path_prefix,
        blank=True,
        null=True,
    )
    hero = VersatileImageField(
        "Hero",
        upload_to=get_group_media_path_prefix,
        blank=True,
        null=True,
    )
    slug = AutoSlugField(populate_from="name", unique=True, db_index=True)
    kind = models.CharField(
        max_length=20, choices=GroupKind.choices, default=GroupKind.PUBLIC
    )
    status = models.CharField(
        max_length=20,
        choices=GroupStatus.choices,
        db_index=True,
        default=GroupStatus.DRAFT,
    )
    country = models.CharField(
        max_length=2, choices=COUNTRIES, default="se", db_index=True
    )
    faq = models.TextField(max_length=10000, null=True, blank=True)

    # Connect to Organisations that are allowed to start Groups/Discussions
    organization = models.ForeignKey(
        "accountio.Organization",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        help_text="The organisation that owns the Group.",
    )

    # Normalized fields that can be updated based on events
    post_count = models.PositiveIntegerField(default=0, db_index=True)
    member_count = models.PositiveIntegerField(default=0, db_index=True)

    objects = GroupQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}, Slug: {self.slug}"

    def get_admins(self):
        return self.member_set.get_role_admins()

    def add_admin(self, user, status=None):
        if status is None:
            status = MemberStatus.MODERATOR_ACCEPTED
        return Member.objects.create(
            group=self, user=user, role=MemberRole.ADMIN, status=status
        )

    def calc_post_count(self):
        self.post_count = self.get_feed().count()
        self.save(update_fields=["post_count"])

    def increase_post_count(self):
        self.post_count = F("post_count") + 1
        self.save(update_fields=["post_count", "updated_at"])

    def decrease_post_count(self):
        if self.post_count > 0:
            self.post_count = F("post_count") - 1
            self.save(update_fields=["post_count"])

    def calc_member_count(self):
        self.member_count = self.get_members().count()
        self.save(update_fields=["member_count", "updated_at"])

    def increase_member_count(self):
        self.member_count = F("member_count") + 1
        self.save(update_fields=["member_count", "updated_at"])

    def decrease_member_count(self):
        if self.member_count > 0:
            self.member_count = F("member_count") - 1
            self.save(update_fields=["member_count"])

    def get_all_members(self):
        return self.member_set.get_status_all()

    def get_members(self):
        return self.member_set.get_status_accepted()

    def add_member(self, user, status=None, referrer=None):
        if status is None:
            status = MemberStatus.PENDING
        return Member.objects.create(
            group=self,
            user=user,
            role=MemberRole.MEMBER,
            status=status,
            referrer=referrer,
        )

    def get_moderators(self):
        roles = [MemberRole.MODERATOR, MemberRole.ADMIN]
        return self.member_set.filter(role__in=roles)

    def add_moderator(
        self, user, role=None, status=None, referrer=None, *args, **kwargs
    ):
        if role is None:
            role = MemberRole.MODERATOR
        if status is None:
            status = MemberStatus.MODERATOR_ACCEPTED
        return Member.objects.create(
            group=self, user=user, role=role, status=status, referrer=referrer
        )

    def is_kind_public(self):
        return self.kind == GroupKind.PUBLIC

    def is_kind_closed(self):
        return self.kind == GroupKind.CLOSED

    def is_kind_secret(self):
        return self.kind == GroupKind.SECRET

    def remove(self):
        now = timezone.now()
        timestamp = now.strftime("%Y%m%d-%H%M%S")
        self.name = f"{self.name}-REMOVED-{timestamp}"
        self.slug = slugify(self.name)
        self.status = GroupStatus.REMOVED
        self.save_dirty_fields()


class Member(BaseModelWithUID):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=MemberRole.choices, db_index=True)
    status = models.CharField(
        max_length=20, choices=MemberStatus.choices, db_index=True
    )
    referrer = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)

    objects = MemberQuerySet.as_manager()

    class Meta:
        unique_together = ("group", "user")
        index_together = ("group", "user")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.get_name()} is {self.role} at {self.group.name}"

    def remove(self, *args, **kwargs):
        self.group.decrease_member_count()
        super(Member, self).delete(*args, **kwargs)


# Signals
post_save.connect(post_save_member, sender=Member)
post_delete.connect(post_delete_member, sender=Member)
