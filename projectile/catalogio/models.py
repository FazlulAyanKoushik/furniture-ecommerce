from django.db import models

from autoslug import AutoSlugField

from common.choices import Currency
from common.models import BaseModelWithUID

from simple_history.models import HistoricalRecords

from versatileimagefield.fields import VersatileImageField

from .choices import (
    ProductChannel,
    ProductCollectionKind,
    ProductCollectionVisibility,
    ProductDiscountKind,
    ProductDiscountStatus,
    ProductDiscountVariant,
    ProductMaterialStatus,
    ProductStatus,
    ServiceKind,
    ServiceStatus,
)
from .managers import MaterialQuerySet, ProductQuerySet, ServiceQuerySet
from .paths import (
    get_brand_image_path,
    get_producmaterial_image_path,
    get_product_image_path,
    get_productcollection_image_path,
    get_productimage_image_path,
)
from .slugifiers import (
    get_brand_slug,
    get_collection_slug,
    get_material_slug,
    get_product_slug,
    get_service_slug,
)


class ProductBrand(BaseModelWithUID):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_brand_slug, unique=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    image = VersatileImageField(upload_to=get_brand_image_path, null=True, blank=True)
    # Foreign Keys
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # Track Changes
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("title", "organization")

    def __str__(self):
        return f"Organization: {self.organization.name}, Brand: {self.title}, Slug: {self.slug}"


class Product(BaseModelWithUID):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_product_slug, unique=True, db_index=True)
    description = models.TextField(blank=True)
    seo_title = models.CharField(verbose_name="SEO Title", max_length=100, blank=True)
    seo_description = models.TextField(verbose_name="SEO Description", blank=True)
    image = VersatileImageField(upload_to=get_product_image_path, null=True, blank=True)
    sku = models.CharField(verbose_name="SKU", max_length=100, blank=True)
    identifier = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=50, choices=ProductStatus.choices)
    published_at = models.DateTimeField(
        verbose_name="Published At", null=True, blank=True
    )
    channels = models.CharField(
        max_length=30,
        choices=ProductChannel.choices,
        default=ProductChannel.OWN_CHANNEL,
    )
    categories = models.JSONField(default=list, null=False, blank=True)
    category = models.CharField(max_length=100, blank=True, db_index=True)
    color = models.CharField(max_length=100, blank=True, db_index=True)
    material = models.CharField(max_length=100, blank=True, db_index=True)

    external_url = models.URLField(unique=True, blank=True, null=True)
    scraped = models.JSONField(default=dict, blank=True)

    # Computed/Aggregated fields
    display_title = models.CharField(
        verbose_name="Display Title", max_length=100, blank=True
    )
    like_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)

    # Foreign Keys
    brand = models.ForeignKey(
        ProductBrand, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    # Custom managers use
    objects = ProductQuerySet.as_manager()

    # Track Changes
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Supplier: {self.organization}, Title: {self.title}, Slug: {self.slug}"

    def set_slug(self):
        self.slug = get_product_slug(self)
        self.save_dirty_fields()


class ProductCollection(BaseModelWithUID):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_collection_slug, unique=True, db_index=True)
    kind = models.CharField(
        max_length=20, choices=ProductCollectionKind.choices, db_index=True
    )
    visibility = models.CharField(
        max_length=20, choices=ProductCollectionVisibility.choices, db_index=True
    )
    product_count = models.PositiveIntegerField(default=0)
    products = models.ManyToManyField(Product, through="ProductCollectionBridge")
    image = VersatileImageField(
        upload_to=get_productcollection_image_path, null=True, blank=True
    )
    # FKs
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)


class ProductImage(BaseModelWithUID):
    image = VersatileImageField(
        upload_to=get_productimage_image_path, null=True, blank=True
    )
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    caption = models.CharField(max_length=100, null=True, blank=True)
    copyright = models.CharField(max_length=100, null=True, blank=True)
    priority = models.BigIntegerField(default=0)

    # FKs
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Product: ({self.product}) - {self.image}, Priority: ({self.priority})"


class ProductAsset(BaseModelWithUID):
    title = models.CharField(max_length=50)
    file = models.FileField()
    extension = models.CharField(max_length=50, null=True, blank=True)
    priority = models.BigIntegerField(default=0)
    # FKs
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # Keep track of changes in model
    history = HistoricalRecords()

    def __str__(self):
        return f"Product: ({self.product}) - {self.title}, Priority: ({self.priority})"


class ProductView(BaseModelWithUID):
    ip_address = models.GenericIPAddressField()

    # FKs
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    collection = models.ForeignKey(
        ProductCollection, null=True, blank=True, on_delete=models.SET_NULL
    )
    brand = models.ForeignKey(
        ProductBrand, null=True, blank=True, on_delete=models.SET_NULL
    )
    product = models.ForeignKey(
        Product, null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ("-created_at",)

    def get_related(self):
        return self.collection or self.brand or self.product


class ProductCollectionBridge(BaseModelWithUID):
    collection = models.ForeignKey(ProductCollection, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("collection", "product")
        index_together = ("collection", "product")

    def __str__(self):
        return f"Collection: ({self.collection}), Product: ({self.product})"


class ProductDiscount(BaseModelWithUID):
    category = models.CharField(max_length=50)
    kind = models.CharField(
        max_length=20,
        choices=ProductDiscountKind.choices,
        default=ProductDiscountKind.DISCOUNT,
    )
    percent = models.DecimalField(max_digits=19, decimal_places=3)
    status = models.CharField(
        max_length=20,
        choices=ProductDiscountStatus.choices,
        default=ProductDiscountStatus.DRAFT,
    )
    variant = models.CharField(
        max_length=20,
        choices=ProductDiscountVariant.choices,
        default=ProductDiscountVariant.PRICE_LIST,
    )
    amount = models.DecimalField(
        max_digits=19, decimal_places=3, null=True, blank=True, default=None
    )
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.SEK
    )

    start_date = models.DateField()
    stop_date = models.DateField(null=True, blank=True)

    # FKs
    user = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    target = models.ForeignKey(
        "accountio.Organization", on_delete=models.CASCADE, related_name="discounts"
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("organization", "target", "category")
        index_together = ("organization", "target", "category")
        ordering = ("-created_at",)


class Service(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="children",
    )
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, populate_from=get_service_slug)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=ServiceStatus.choices,
        default=ServiceStatus.DRAFT,
        db_index=True,
    )
    kind = models.CharField(
        max_length=30,
        choices=ServiceKind.choices,
        default=ServiceKind.SERVICE,
        db_index=True,
    )

    # Managers
    objects = ServiceQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Services"

    def __str__(self):
        return f"UID:{self.uid}, Title: {self.title}"


class Material(BaseModelWithUID):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from=get_material_slug, unique=True, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=ProductMaterialStatus.choices,
        default=ProductMaterialStatus.DRAFT,
    )
    image = VersatileImageField(
        upload_to=get_producmaterial_image_path, null=True, blank=True
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)

    # Managers
    objects = MaterialQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class ProductMaterialConnector(BaseModelWithUID):
    product = models.ForeignKey("catalogio.Product", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("material", "product")

    def __str__(self):
        return f"Product: {self.product.title}, Material: {self.material.name}"


class OrganizationServiceConnector(BaseModelWithUID):
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)
        index_together = (
            "organization",
            "service",
        )
        unique_together = (
            "organization",
            "service",
        )

    def __str__(self):
        return f"Organization: {self.organization.name}, Service: {self.service.title}"
