from django.contrib import admin

from .models import NewsdeskPost, NewsPostAccess


@admin.register(NewsdeskPost)
class NewsdeskPostAdmin(admin.ModelAdmin):
    list_display = [
        "organization",
        "title",
        "slug",
        "updated_at",
    ]


@admin.register(NewsPostAccess)
class NewsPostAccessAdmin(admin.ModelAdmin):
    list_display = [
        "newspost",
        "partner",
        "user",
        "kind",
    ]
