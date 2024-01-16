from django.db import models


class OrganizationInviteResponse(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    DECLINED = "DECLINED", "Declined"
    BLOCKED = "BLOCKED", "Blocked"
