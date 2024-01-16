from django.db import models


class UserPhoneStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"


class UserPhoneOTPStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    CONSUMED = "CONSUMED", "Consumed"