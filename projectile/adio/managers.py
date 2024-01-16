import logging

from django.db import models

from adio.choices import AdOrganizationStatus, AdProductStatus, AdProjectStatus

logger = logging.getLogger(__name__)


class AdOrganizationQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=AdOrganizationStatus.ACTIVE)

    def get_status_fair(self):
        statuses = [
            AdOrganizationStatus.PENDING,
            AdOrganizationStatus.ACTIVE,
        ]
        return self.filter(status__in=statuses)


class AdProductQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=AdProductStatus.ACTIVE)

    def get_status_fair(self):
        statuses = [
            AdProductStatus.PENDING,
            AdProductStatus.ACTIVE,
        ]
        return self.filter(status__in=statuses)


class AdProjectQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=AdProjectStatus.ACTIVE)

    def get_status_fair(self):
        statuses = [
            AdProjectStatus.PENDING,
            AdProjectStatus.ACTIVE,
        ]
        return self.filter(status__in=statuses)
