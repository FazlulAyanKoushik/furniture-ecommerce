from django.db import models

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords

from common.models import BaseModelWithUID

from .managers import FileItemQuerySet
from .choices import (
    FileExtension,
    FileKind,
    FileVisibility,
    FileStatus,
    FileItemConnectorKind,
    FileItemAccessKind,
)

from .paths import (
    get_fileitem_file_path,
)
from collabio.slugifiers import get_organization_slug


class FileItem(BaseModelWithUID):
    fileitem = models.FileField(upload_to=get_fileitem_file_path)
    size = models.PositiveIntegerField(default=0)
    dotextension = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=20, choices=FileKind.choices)
    extension = models.CharField(
        max_length=20, choices=FileExtension.choices, default=FileExtension.OTHER
    )
    visibility = models.CharField(max_length=20, choices=FileVisibility.choices)
    status = models.CharField(max_length=20, choices=FileStatus.choices)

    # FKs
    user = models.ForeignKey(
        "core.User", null=True, blank=True, on_delete=models.SET_NULL
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    organization_slug = AutoSlugField(
        populate_from=get_organization_slug, db_index=True
    )
    # Use custom managers
    objects = FileItemQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Organization: ({self.organization}), File: {self.fileitem}"


class FileItemConnector(BaseModelWithUID):
    fileitem = models.ForeignKey(FileItem, on_delete=models.CASCADE)
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
        default=FileItemConnectorKind.UNDEFINED,
        choices=FileItemConnectorKind.choices,
        db_index=True,
    )
    # FKs
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    organization_slug = AutoSlugField(
        populate_from=get_organization_slug, db_index=True
    )
    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            ("fileitem", "group"),
            ("fileitem", "newspost"),
            ("fileitem", "product"),
            ("fileitem", "project"),
        )
        unique_together = (
            ("fileitem", "group"),
            ("fileitem", "newspost"),
            ("fileitem", "product"),
            ("fileitem", "project"),
        )

    def __str__(self):
        return f"Product: ({self.product}), File: {self.fileitem}"


class FileItemAccess(BaseModelWithUID):
    """
    Keep track of who has access to a FileItem
    * Can be shared with a Partner (an accountio.Organization instance)
    * Can be shared with a User (a core.User instance)
    """

    fileitem = models.ForeignKey(FileItem, on_delete=models.CASCADE)
    partner = models.ForeignKey(
        "accountio.Organization", null=True, blank=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "core.User", null=True, blank=True, on_delete=models.CASCADE
    )
    kind = models.CharField(
        max_length=20,
        choices=FileItemAccessKind.choices,
        default=FileItemAccessKind.PARTNER,
    )

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            ("fileitem", "partner"),
            ("fileitem", "user"),
        )
        unique_together = (
            ("fileitem", "partner"),
            ("fileitem", "user"),
        )

    def __str__(self):
        return f"Partner: ({self.partner}), File: {self.fileitem}"
