from django.db import models

from autoslug import AutoSlugField

from collabio.slugifiers import get_organization_slug

from common.models import BaseModelWithUID

from simple_history.models import HistoricalRecords

from versatileimagefield.fields import PPOIField, VersatileImageField

from .choices import (
    MediaImageConnectorKind,
    MediaImageKind,
    MediaImageSpot,
    MediaImageStatus,
)
from .managers import MediaImageConnectorQuerySet, MediaImageQuerySet

from .paths import get_mediaimage_image_path


class MediaImage(BaseModelWithUID):
    image = VersatileImageField(
        upload_to=get_mediaimage_image_path,
        width_field="width",
        height_field="height",
        ppoi_field="ppoi",
    )
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    ppoi = PPOIField()
    title = models.CharField(max_length=100, blank=True)
    caption = models.CharField(max_length=100, blank=True)
    copyright = models.CharField(max_length=100, blank=True)
    priority = models.BigIntegerField(default=0)
    kind = models.CharField(
        max_length=20, choices=MediaImageKind.choices, db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=MediaImageStatus.choices,
        default=MediaImageStatus.PUBLISHED,
        db_index=True,
    )
    spot = models.CharField(
        max_length=20,
        choices=MediaImageSpot.choices,
        default=MediaImageSpot.UNDEFINED,
        blank=True,
    )

    # FKs
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    organization_slug = AutoSlugField(
        populate_from=get_organization_slug, db_index=True
    )
    # use custom managers
    objects = MediaImageQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Organization: ({self.organization}), Image: {self.image}, Priority: {self.priority}"


class MediaImageConnector(BaseModelWithUID):
    # FKs
    image = models.ForeignKey("mediaroomio.MediaImage", on_delete=models.CASCADE)
    group = models.ForeignKey(
        "gruppio.Group", blank=True, null=True, on_delete=models.SET_NULL
    )
    newspost = models.ForeignKey(
        "newsdeskio.NewsdeskPost", blank=True, null=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        "catalogio.Product", blank=True, null=True, on_delete=models.SET_NULL
    )
    project = models.ForeignKey(
        "collabio.Project", blank=True, null=True, on_delete=models.SET_NULL
    )
    kind = models.CharField(
        max_length=20,
        default=MediaImageConnectorKind.UNDEFINED,
        choices=MediaImageConnectorKind.choices,
        db_index=True,
    )

    # FKs
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    organization_slug = AutoSlugField(
        populate_from=get_organization_slug, db_index=True
    )
    # use custom managers
    objects = MediaImageConnectorQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            ("image", "group"),
            ("image", "newspost"),
            ("image", "product"),
            ("image", "project"),
        )
        unique_together = (
            ("image", "group"),
            ("image", "newspost"),
            ("image", "product"),
            ("image", "project"),
        )

    def __str__(self):
        return f"Product: ({self.product}), Image: {self.image}"


class ShowRoomImageConnector(BaseModelWithUID):
    image = models.ForeignKey(
        "mediaroomio.MediaImage",
        on_delete=models.CASCADE,
        related_name="showroom_image",
    )
    gallery_image = models.ForeignKey(
        "mediaroomio.MediaImage",
        on_delete=models.SET_NULL,
        related_name="gallery_images",
        null=True,
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        unique_together = (("image", "gallery_image"),)
