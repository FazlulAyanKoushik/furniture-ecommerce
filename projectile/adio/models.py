from django.db import models

from autoslug.fields import AutoSlugField

from common.models import BaseModelWithUID

from paymentio.models import AdFeature

from .choices import (
    AdOrganizationStatus,
    AdProductStatus,
    AdProjectStatus,
    DaysValidityStatus,
)
from .managers import (
    AdOrganizationQuerySet,
    AdProductQuerySet,
    AdProjectQuerySet,
)
from .utils import get_ad_organization_slug, get_ad_product_slug, get_ad_project_slug


class AdProduct(BaseModelWithUID):
    adfeature = models.ForeignKey(AdFeature, on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from=get_ad_product_slug, unique=True, db_index=True)
    product = models.ForeignKey("catalogio.Product", on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    start_date = models.DateField()
    ad_days = models.CharField(
        max_length=20, choices=DaysValidityStatus.choices, db_index=True
    )
    stop_date = models.DateField()
    total_price = models.DecimalField(max_digits=19, decimal_places=3, default=0)
    status = models.CharField(
        max_length=20,
        choices=AdProductStatus.choices,
        default=AdProductStatus.PENDING,
        db_index=True,
    )
    view_count = models.PositiveBigIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)

    objects = AdProductQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Product: {self.product.title}"

    def increment_count(self):
        self.view_count += 1
        self.click_count += 1
        self.save_dirty_fields()


class AdProject(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_ad_project_slug, unique=True, db_index=True)
    adfeature = models.ForeignKey(AdFeature, on_delete=models.CASCADE)
    project = models.ForeignKey("collabio.Project", on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    start_date = models.DateField()
    ad_days = models.CharField(
        max_length=20, choices=DaysValidityStatus.choices, db_index=True
    )
    stop_date = models.DateField()
    total_price = models.DecimalField(max_digits=19, decimal_places=3, default=0)

    status = models.CharField(
        max_length=20,
        choices=AdProjectStatus.choices,
        default=AdProjectStatus.PENDING,
        db_index=True,
    )
    view_count = models.PositiveBigIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)

    objects = AdProjectQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Project: {self.project.title}"

    def increment_count(self):
        self.view_count += 1
        self.click_count += 1
        self.save_dirty_fields()


class AdOrganization(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_ad_organization_slug, unique=True, db_index=True
    )
    adfeature = models.ForeignKey(AdFeature, on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    start_date = models.DateField()
    ad_days = models.CharField(
        max_length=20, choices=DaysValidityStatus.choices, db_index=True
    )
    stop_date = models.DateField()
    total_price = models.DecimalField(max_digits=19, decimal_places=3, default=0)
    status = models.CharField(
        max_length=20,
        choices=AdOrganizationStatus.choices,
        default=AdOrganizationStatus.PENDING,
        db_index=True,
    )
    view_count = models.PositiveBigIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)

    objects = AdOrganizationQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Organization: {self.organization.name}"

    def increment_count(self):
        self.view_count += 1
        self.click_count += 1
        self.save_dirty_fields()
