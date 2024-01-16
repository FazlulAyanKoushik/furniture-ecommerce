from django.contrib import admin

from .models import PotentialLead, LeadContact


class LeadContactInline(admin.TabularInline):
    model = LeadContact
    extra = 1


class PotentialLeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization_no",
        "address",
        "postal_code",
        "postal_area",
        "country",
        "phone",
        "website",
        "status",
    )
    search_fields = ("name", "website", "phone")
    list_filter = ("status", "country", "updated_at")
    inlines = [
        LeadContactInline,
    ]


admin.site.register(PotentialLead, PotentialLeadAdmin)
