from django.db import models


class PopularOrganizationStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PLACEHOLDER = "PLACEHOLDER", "Placeholder"
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class PopularProductStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class PopularProjectStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"
