from django.db import models


class GroupKind(models.TextChoices):
    PUBLIC = "PUBLIC", "Public"
    CLOSED = "CLOSED", "Closed"
    SECRET = "SECRET", "Secret"


class GroupStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    FROZEN = "FROZEN", "Frozen"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class MemberRole(models.TextChoices):
    SPECTATOR = "SPECTATOR", "Spectator"
    MEMBER = "MEMBER", "Member"
    MODERATOR = "MODERATOR", "Moderator"
    ADMIN = "ADMIN", "Admin"


class MemberStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    MODERATOR_ACCEPTED = "MODERATOR_ACCEPTED", "Moderator Accepted"
    MODERATOR_REJECTED = "MODERATOR_REJECTED", "Moderator Rejected"
    USER_ACCEPTED = "USER_ACCEPTED", "User Accepted"
    USER_REJECTED = "USER_REJECTED", "User Rejected"
