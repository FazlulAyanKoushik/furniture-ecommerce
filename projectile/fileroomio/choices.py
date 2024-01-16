from django.db import models


class FileKind(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"
    PRICE_LIST = "PRICE_LIST", "Price List"
    BROCHURE = "BROCHURE", "Brochure"
    CATALOG = "CATALOG", "Catalog"
    PRODUCT_INFORMATION = "PRODUCT_INFORMATION", "Product Information"
    DRAWING = "DRAWING", "Drawing"
    CERTIFICATE = "CERTIFICATE", "Certificate"
    CARE_INSTRUCTION = "CARE_INSTRUCTION", "Care Instruction"
    PRESS = "PRESS", "Press"
    OTHER = "OTHER", "Other"


class FileExtension(models.TextChoices):
    EXCEL = "EXCEL", "Excel"
    POWERPOINT = "POWERPOINT", "Powerpoint"
    WORD = "WORD", "Word"
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"
    OTHER = "OTHER", "Other"


class FileStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    UNPUBLISHED = "UNPUBLISHED", "Unpublished"
    REMOVED = "REMOVED", "Removed"


class FileVisibility(models.TextChoices):
    SECRET = "SECRET", "Secret"
    PRIVATE = "PRIVATE", "Private"
    PUBLIC = "PUBLIC", "Public"


class FileItemConnectorKind(models.TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    GROUP = "GROUP", "Group"
    NEWS_POST = "NEWS_POST", "News Post"
    PRODUCT = "PRODUCT", "Product"
    PROJECT = "PROJECT", "Project"


class FileItemAccessKind(models.TextChoices):
    PARTNER = "PARTNER", "Partner"
    USER = "USER", "User"
