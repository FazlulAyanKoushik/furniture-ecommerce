from django.contrib import admin

from .models import Tag, TagConnector


class TagInline(admin.TabularInline):
    model = Tag
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "name",
        "slug",
        "parent",
        "i18n",
        "status",
        "updated_at",
    ]
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["name", "slug"]
    inlines = [TagInline]


admin.site.register(Tag, TagAdmin)
admin.site.register(TagConnector)
