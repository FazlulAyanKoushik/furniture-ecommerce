from django.db import models


class ProjectVisibility(models.TextChoices):
    SECRET = "SECRET", "Secret"
    PRIVATE = "PRIVATE", "Private"
    PUBLIC = "PUBLIC", "Public"
    GLOBAL = "GLOBAL", "Global"


class ProjectPhase(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ONGOING = "ONGOING", "Ongoing"
    FINISHED = "FINISHED", "Finished"


class ProjectStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    ARCHIVED = "ARCHIVED", "Archived"
    REMOVED = "REMOVED", "Removed"


class ProjectParticipantStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    DECLINED = "DECLINED", "Declined"
    SUSPENDED = "SUSPENDED", "Suspended"
    ARCHIVED = "ARCHIVED", "Archived"
    REJECTED = "REJECTED", "Rejected"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"
