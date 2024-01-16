import logging

from django.db import models

from .choices import (
    PopularOrganizationStatus,
    PopularProductStatus,
    PopularProjectStatus,
)

logger = logging.getLogger(__name__)


class PopularOrganizationQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=PopularOrganizationStatus.ACTIVE)

    def get_popular(self):
        return (
            self.get_status_active().exclude(organization__image="").order_by("?")[:16]
        )


class PopularProductQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=PopularProductStatus.PUBLISHED)

    def get_popular(self):
        return (
            self.get_status_active()
            .filter(product__view_count__gt=0)
            .exclude(product__image="")
            .order_by("?")[:16]
        )


class PopularProjectQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=PopularProjectStatus.ACTIVE)

    def get_popular(self):
        return self.get_status_active().exclude(project__image="").order_by("?")[:16]
