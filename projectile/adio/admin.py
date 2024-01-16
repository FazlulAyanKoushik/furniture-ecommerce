from django.contrib import admin

from .models import AdOrganization, AdProduct, AdProject


@admin.register(AdOrganization)
class AdOrganizationAdmin(admin.ModelAdmin):
    list_display = [
        "organization_",
        "start_date",
        "stop_date",
        "created_at",
    ]

    def organization_(self, object_):
        return object_.organization.name


@admin.register(AdProduct)
class AdProductAdmin(admin.ModelAdmin):
    list_display = ["product_", "start_date", "stop_date", "created_at"]

    def product_(self, object_):
        return object_.product.title


@admin.register(AdProject)
class AdProjectAdmin(admin.ModelAdmin):
    list_display = ["project_", "start_date", "stop_date", "created_at"]

    def project_(self, object_):
        return object_.project.title
