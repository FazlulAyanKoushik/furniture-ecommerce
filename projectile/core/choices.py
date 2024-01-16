from django.db import models


class UserEmailStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"


class UserGender(models.TextChoices):
    FEMALE = "FEMALE", "Female"
    MALE = "MALE", "Male"
    OTHER = "OTHER", "Other"


class UserObjective(models.TextChoices):
    UNKNOWN = "UNKNOWN", "Unknown"
    SUPPLIER = "SUPPLIER", "Supplier"
    RETAILER = "RETAILER", "Retailer"
    ARCHITECT = "ARCHITECT", "Architect"
    OTHER = "OTHER", "Other"


class UserStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PLACEHOLDER = "PLACEHOLDER", "Placeholder"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    PAUSED = "PAUSED", "Paused"
    REMOVED = "REMOVED", "Removed"
