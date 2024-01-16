from django.db import models


class MediaImageKind(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"


class MediaImageSpot(models.TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    SHOWROOM = "SHOWROOM", "Showroom"


class MediaImageConnectorKind(models.TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    GROUP = "GROUP", "Group"
    NEWS_POST = "NEWSPOST", "News Post"
    PRODUCT = "PRODUCT", "Product"
    PROJECT = "PROJECT", "Project"


class MediaImageStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"
