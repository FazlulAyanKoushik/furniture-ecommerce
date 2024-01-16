from django.contrib import admin

from .models import (
    Material,
    OrganizationServiceConnector,
    Product,
    ProductBrand,
    ProductCollection,
    ProductDiscount,
    ProductMaterialConnector,
    ProductView,
    Service,
)


@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "title",
        "slug",
        "updated_at",
    ]


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "title",
        "slug",
        "updated_at",
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "brand",
        "title",
        "slug",
        "status",
        "updated_at",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "title",
    ]


@admin.register(ProductDiscount)
class ProductDiscountAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "organization",
        "target",
        "kind",
        "percent",
        "status",
        "start_date",
        "stop_date",
    ]
    list_filter = [
        "kind",
        "status",
        "start_date",
        "stop_date",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "title",
    ]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "status",
        "created_at",
        "updated_at",
    ]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "status",
        "created_at",
    ]


@admin.register(ProductMaterialConnector)
class MaterialConnectorAdmin(admin.ModelAdmin):
    list_display = [
        "_product",
        "_material",
    ]

    def _material(self, obj):
        return obj.material.name

    def _product(self, obj):
        return obj.product.title


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = [
        "_organization",
        "_product",
    ]

    def _organization(self, object):
        return object.organization.name

    def _product(self, object):
        return object.product.title


@admin.register(OrganizationServiceConnector)
class OrganizationService(admin.ModelAdmin):
    list_display = ["organization", "service", "created_at"]
