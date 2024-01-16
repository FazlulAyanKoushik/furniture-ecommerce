from django.db import models


class AdOrganizationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"


class AdProductStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"


class AdProjectStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"


class DaysValidityStatus(models.TextChoices):
    DAYS_60 = "60_DAYS", "60 Days"
    DAYS_30 = "30_DAYS", "30 Days"
