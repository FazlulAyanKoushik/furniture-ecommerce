import logging

from django.db import models

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from .choices import (
    PopularOrganizationStatus,
    PopularProductStatus,
    PopularProjectStatus,
)
from .managers import (
    PopularOrganizationQuerySet,
    PopularProductQuerySet,
    PopularProjectQuerySet,
)
from .utils import (
    get_popular_organization_slug,
    get_popular_product_slug,
    get_popular_project_slug,
)


logger = logging.getLogger(__name__)


class PopularOrganization(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_popular_organization_slug, unique=True, db_index=True
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=PopularOrganizationStatus.choices,
        default=PopularOrganizationStatus.ACTIVE,
    )

    # Custom managers use
    objects = PopularOrganizationQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.organization.name}"


class PopularProduct(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_popular_product_slug, unique=True, db_index=True
    )
    product = models.ForeignKey("catalogio.Product", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=PopularProductStatus.choices,
        default=PopularProductStatus.PUBLISHED,
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    # Custom managers use
    objects = PopularProductQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.product.title}"


class PopularProject(BaseModelWithUID):
    slug = AutoSlugField(
        populate_from=get_popular_project_slug, unique=True, db_index=True
    )
    project = models.ForeignKey("collabio.Project", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=PopularProjectStatus.choices,
        default=PopularProjectStatus.ACTIVE,
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    # Custom managers use
    objects = PopularProjectQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.project.title}"
