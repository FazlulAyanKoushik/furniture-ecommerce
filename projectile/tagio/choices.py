from django.db import models


class TagEntity(models.TextChoices):
    ORGANIZATION = "ORGANIZATION", "Organization"
    PRODUCT = "PRODUCT", "Product"
    USER = "USER", "User"


class TagCategory(models.TextChoices):
    COLOR = "COLOR", "Color"
    INDUSTRY = "INDUSTRY", "Industry"
    PRODUCT = "PRODUCT", "Product"
    MATERIAL = "MATERIAL", "Material"
    TEXTILE = "TEXTILE", "Textile"
    FABRIC = "FABRIC", "Fabric"
    WOOD = "WOOD", "Wood"
    PLASTIC = "PLASTIC", "Plastic"
    METAL = "METAL", "Metal"


class TagStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    ARCHIVED = "ARCHIVED", "Archived"
    REMOVED = "REMOVED", "Removed"
