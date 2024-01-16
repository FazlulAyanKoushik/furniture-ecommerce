import logging

from django.db import models

from common.models import BaseModelWithUID

logger = logging.getLogger(__name__)


class ScrapProductData(BaseModelWithUID):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_link = models.CharField(max_length=400, blank=True, null=True)
    product_link = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Scrapped Product"
        verbose_name_plural = "Scrapped Products"
