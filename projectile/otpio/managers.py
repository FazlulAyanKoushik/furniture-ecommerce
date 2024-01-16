import logging

from django.db import models

from .choices import UserPhoneStatus

logger = logging.getLogger(__name__)


class UserPhoneQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=UserPhoneStatus.ACTIVE)

    def get_status_editable(self):
        statuses = [
            UserPhoneStatus.PENDING,
            UserPhoneStatus.ACTIVE,
        ]
        return self.filter(status__in=statuses)
