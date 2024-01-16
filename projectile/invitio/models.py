import uuid

from django.conf import settings
from django.db import models

from common.models import BaseModelWithUID

from .choices import OrganizationInviteResponse


class OrganizationInvite(BaseModelWithUID):
    responder = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="invite_replies",
    )
    target = models.ForeignKey(
        "accountio.Organization", on_delete=models.CASCADE, related_name="invites"
    )
    message = models.TextField(blank=True)
    response = models.CharField(
        max_length=20,
        default=OrganizationInviteResponse.PENDING,
        choices=OrganizationInviteResponse.choices,
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # FKs
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("organization", "target")
        index_together = ("organization", "target")

    def __str__(self) -> str:
        return f"Organization: {self.organization}, Target: ({self.target})"
