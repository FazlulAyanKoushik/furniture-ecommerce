from django.db import models


class ProductCollectionKind(models.TextChoices):
    COLLECTION = "COLLECTION", "Collection"
    CATEGORY = "CATEGORY", "Category"


class ProductCollectionVisibility(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    PUBLIC = "PUBLIC", "Public"


class ProductStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class ProductDiscountKind(models.TextChoices):
    DISCOUNT = "DISCOUNT", "Discount"
    NET_PRICE = "NET_PRICE", "Net Price"


class ProductDiscountStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"


class ProductDiscountVariant(models.TextChoices):
    PRICE_LIST = "PRICE_LIST", "Price List"
    AMOUNT = "AMOUNT", "Amount"


class ServiceStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class ProductMaterialStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"
    ARCHIVED = "ARCHIVED", "Archived"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"



class ProductChannel(models.TextChoices):
    OWN_CHANNEL = "OWN_CHANNEL", "Own Channel"
    PARTNERS_CHANNELS = "PARTNERS_CHANNELS", "Partners Channels"
    ALL_CHANNELS = "ALL_CHANNELS", "All Channels"


class ServiceKind(models.TextChoices):
    SERVICE = "SERVICE", "Service"
    PRESET_SERVICE = "PRESET_SERVICE", "Preset Service"