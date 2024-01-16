import logging

from django.db import models

from .choices import MediaImageKind, MediaImageSpot, MediaImageConnectorKind

logger = logging.getLogger(__name__)


class MediaImageQuerySet(models.QuerySet):
    def get_kind_image(self):
        return self.filter(kind=MediaImageKind.IMAGE)

    def get_kind_editable(self):
        kind = [MediaImageKind.IMAGE, MediaImageKind.VIDEO]
        return self.filter(kind__in=kind)

    def get_spot_showroom(self):
        return self.filter(spot=MediaImageSpot.SHOWROOM)


class MediaImageConnectorQuerySet(models.QuerySet):
    def get_kind_group(self):
        return self.filter(kind=MediaImageConnectorKind.GROUP)

    def get_kind_news_post(self):
        return self.filter(kind=MediaImageConnectorKind.NEWS_POST)

    def get_kind_product(self):
        return self.filter(kind=MediaImageConnectorKind.PRODUCT)

    def get_kind_project(self):
        return self.filter(kind=MediaImageConnectorKind.PROJECT)
