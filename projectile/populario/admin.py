from django.contrib import admin

from .models import PopularOrganization, PopularProduct, PopularProject


@admin.register(PopularOrganization)
class PopularOrganizationAdmin(admin.ModelAdmin):
    list_display = ["organization_", "created_at"]

    def organization_(self, object):
        return object.organization.name


@admin.register(PopularProduct)
class PopularProductAdmin(admin.ModelAdmin):
    list_display = ["product_", "created_at"]

    def product_(self, object):
        return object.product.title


@admin.register(PopularProject)
class PopularProjectAdmin(admin.ModelAdmin):
    list_display = ["project_", "created_at"]

    def project_(self, object):
        return object.project.title
