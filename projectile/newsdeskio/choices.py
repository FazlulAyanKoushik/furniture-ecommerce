from django.db import models


class NewsdeskPostKind(models.TextChoices):
    EVENT = "EVENT", "Event"
    NEWS = "NEWS", "News"


class NewsdeskPostStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class NewsPostAccessKind(models.TextChoices):
    PARTNER = "PARTNER", "Partner"
    USER = "USER", "User"
