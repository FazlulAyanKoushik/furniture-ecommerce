import uuid

from django.conf import settings
from django.db import models

from autoslug import AutoSlugField
from simple_history.models import HistoricalRecords
from versatileimagefield.fields import VersatileImageField

from common.lists import COUNTRIES
from common.models import BaseModelWithUID

from .managers import ProjectQuerySet

from .choices import ProjectPhase, ProjectStatus, ProjectVisibility, ProjectParticipantStatus

from .paths import get_project_image_path
from .slugifiers import get_project_slug, get_organization_slug


class Project(BaseModelWithUID):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_project_slug, unique=True, db_index=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    country = models.CharField(
        max_length=2, choices=COUNTRIES, default="se", db_index=True
    )
    image = VersatileImageField(upload_to=get_project_image_path)
    phase = models.CharField(max_length=20, choices=ProjectPhase.choices)
    status = models.CharField(max_length=20, choices=ProjectStatus.choices)
    visibility = models.CharField(max_length=20, choices=ProjectVisibility.choices)
    date_start = models.DateField(null=True, blank=True)
    date_stop = models.DateField(null=True, blank=True)

    # FKs
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    organization_slug = AutoSlugField(
        populate_from=get_organization_slug, db_index=True
    )
    # Custom managers use
    objects = ProjectQuerySet.as_manager()
    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"Title: {self.title}, Organization: ({self.organization})"


class ProjectParticipant(BaseModelWithUID):
    role = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=ProjectParticipantStatus.choices,
        db_index=True,
        default=ProjectParticipantStatus.PENDING,
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reminded_at = models.DateTimeField(null=True, blank=True)
    # FKs
    project = models.ForeignKey("collabio.Project", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("project", "user")

    def __str__(self) -> str:
        return f"Project: {self.project}, User: {self.user}"


class ProjectProduct(BaseModelWithUID):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    product = models.ForeignKey("catalogio.Product", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("project", "product")