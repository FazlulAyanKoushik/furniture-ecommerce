import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from versatileimagefield.fields import VersatileImageField

from .choices import CustomerServiceStatus

from .managers import CustomerServiceQuerySet

from .utils import (
    get_customer_service_slug,
    get_faq_slug,
    get_faq_media_path_prefix,
    get_organization_media_path_prefix,
)

logger = logging.getLogger(__name__)


class CustomerService(BaseModelWithUID):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=get_customer_service_slug, unique=True, db_index=True
    )
    description = models.TextField(blank=True)
    image = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=CustomerServiceStatus.choices,
        db_index=True,
        default=CustomerServiceStatus.ACTIVE,
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    # Managers
    objects = CustomerServiceQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class FAQ(BaseModelWithUID):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from=get_faq_slug, unique=True, db_index=True)
    segment = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100)
    image = VersatileImageField(upload_to=get_faq_media_path_prefix, blank=True)
    youtube_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField(blank=True)
    priority = models.IntegerField(
        default=0, help_text="Higher number is higher priority."
    )

    def __str__(self):
        return f"UID: {self.uid} - Title: {self.title}"
