from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Descendant,
    Organization,
    OrganizationUser,
)


class OrganizationUserInline(admin.TabularInline):
    model = OrganizationUser
    extra = 1
    autocomplete_fields = [
        "organization",
        "referrer",
    ]


@admin.register(Organization)
class OrganizationAdmin(SimpleHistoryAdmin):
    list_display = [
        "name",
        "slug",
        "registration_no",
        "kind",
        "country",
        "status",
        "updated_at",
    ]
    list_filter = [
        "status",
        "kind",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
    ]
    autocomplete_fields = [
        "parent",
    ]
    inlines = [OrganizationUserInline]


@admin.register(Descendant)
class DescendantAdmin(SimpleHistoryAdmin):
    list_display = ["child", "parent", "updated_at"]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    autocomplete_fields = [
        "parent",
        "child",
    ]


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "_organization",
        "role",
        "status",
        "is_default",
        "_referrer",
        "updated_at",
    ]
    list_filter = [
        "status",
        "created_at",
        "updated_at",
    ]
    ordering = ("-created_at",)
    search_fields = (
        "user__email",
        "organization__name",
    )

    def _organization(self, instance):
        return instance.organization.name

    def _referrer(self, instance):
        referrer = instance.referrer
        return referrer.user.email if referrer else referrer
