import logging

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from .choices import TagCategory, TagEntity, TagStatus
from .managers import TagQuerySet
from .signals import post_save_tag, post_delete_tag
from .utils import get_tag_slug

logger = logging.getLogger(__name__)


class Tag(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    category = models.CharField(
        max_length=40, choices=TagCategory.choices, db_index=True
    )
    name = models.CharField(max_length=100)
    i18n = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_tag_slug, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=TagStatus.choices, db_index=True)
    objects = TagQuerySet.as_manager()

    class Meta:
        ordering = (
            "category",
            "name",
        )

    def __str__(self):
        return f"Category: {TagCategory(self.category).label}, Name: {self.name}, slug: {self.slug}"


class TagConnector(BaseModelWithUID):
    organization = models.ForeignKey(
        "accountio.Organization", on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        "catalogio.Product", on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, null=True, blank=True
    )
    entity = models.CharField(max_length=20, choices=TagEntity.choices, db_index=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tag Connector"
        ordering = ("-created_at",)
        unique_together = (
            (
                "organization",
                "tag",
            ),
            (
                "product",
                "tag",
            ),
            (
                "user",
                "tag",
            ),
        )
        index_together = (
            (
                "organization",
                "tag",
            ),
            (
                "product",
                "tag",
            ),
            (
                "user",
                "tag",
            ),
        )


post_save.connect(post_save_tag, sender=Tag)
post_delete.connect(post_delete_tag, sender=Tag)
