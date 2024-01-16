from django.db import models


class SubscriptionPlanStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    HIDDEN = "HIDDEN", "Hidden"
    ARCHIVED = "ARCHIVED", "Archived"
    REMOVED = "REMOVED", "Removed"


class SubscriptionSessionStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    CLOSED = "CLOSED", "Closed"


class SubscriptionTransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCEEDED = (
        "SUCCEEDED",
        "Succeeded",
    )
    CANCELLED = "CANCELLED", "Cancelled"
    FAILED = "FAILED", "Failed"


class AdFeatureKind(models.TextChoices):
    PRODUCT = "PRODUCT", "Product"
    PROJECT = "PROJECT", "Project"
    ORGANIZATION = "ORGANIZATION", "Organization"


class SingleTransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCEEDED = (
        "SUCCEEDED",
        "Succeeded",
    )
    CANCELLED = "CANCELLED", "Cancelled"
    FAILED = "FAILED", "Failed"


class SingleSessionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    CLOSED = "CLOSED", "Closed"


class SingleSessionKind(models.TextChoices):
    PRODUCT = "PRODUCT", "Product"
    PROJECT = "PROJECT", "Project"
    ORGANIZATION = "ORGANIZATION", "Organization"
