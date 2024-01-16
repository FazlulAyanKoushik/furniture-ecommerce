import logging

from django.db import models

from .choices import (
    ProductMaterialStatus,
    ProductStatus,
    ServiceStatus,
    ServiceKind,
    ProductChannel,
)

logger = logging.getLogger(__name__)


class ProductQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=ProductStatus.PUBLISHED)

    def get_status_editable(self):
        statuses = [
            ProductStatus.DRAFT,
            ProductStatus.PUBLISHED,
            ProductStatus.UNPUBLISHED,
            ProductStatus.ARCHIVED,
            ProductStatus.HIDDEN,
        ]
        return self.filter(status__in=statuses)

    def get_own_channels(self):
        channels = [ProductChannel.OWN_CHANNEL, ProductChannel.ALL_CHANNELS]
        return self.filter(channels__in=channels)

    def get_partners_channels(self):
        channels = [ProductChannel.PARTNERS_CHANNELS, ProductChannel.ALL_CHANNELS]
        return self.filter(channels__in=channels)


class ServiceQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=ServiceStatus.ACTIVE)

    def get_kind_preset_service(self):
        return self.filter(kind=ServiceKind.PRESET_SERVICE, status=ServiceStatus.ACTIVE)

    def get_status_editable(self):
        statuses = [
            ServiceStatus.ACTIVE,
            ServiceStatus.DRAFT,
            ServiceStatus.ARCHIVED,
            ServiceStatus.HIDDEN,
        ]
        return self.filter(status__in=statuses)


class MaterialQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=ProductMaterialStatus.PUBLISHED)

    def get_status_editable(self):
        statuses = [
            ProductMaterialStatus.DRAFT,
            ProductMaterialStatus.PUBLISHED,
            ProductMaterialStatus.UNPUBLISHED,
            ProductMaterialStatus.ARCHIVED,
            ProductMaterialStatus.HIDDEN,
        ]
        return self.filter(status__in=statuses)
