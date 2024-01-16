from django.contrib import admin
from .models import CustomerService, FAQ


@admin.register(CustomerService)
class CustomerServiceAdmin(admin.ModelAdmin):
    list_display = [        
        "organization_",
        "status",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    ordering = ("-created_at",)
    search_fields = ("organization__name",)

    def organization_(self, instance):
        return instance.organization.name


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):   
    list_display = [
        "slug",
        "title",
        "category",
        "segment",
        "created_at",
        "updated_at",
    ]
