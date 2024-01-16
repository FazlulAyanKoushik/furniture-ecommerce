from django.contrib import admin

from .models import OrganizationInvite


@admin.register(OrganizationInvite)
class OrganizationInviteAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "sender",
        "target",
        "responder",
        "response",
        "message",
        "updated_at",
    ]
    list_filter = [
        "response",
        "created_at",
        "updated_at",
    ]
