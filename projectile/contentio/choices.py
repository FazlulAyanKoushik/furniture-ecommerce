from django.db import models


class CustomerServiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    ARCHIVED = "ARCHIVED", "Archived"
    REMOVED = "REMOVED", "Removed"
