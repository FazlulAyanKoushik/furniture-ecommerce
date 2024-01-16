from django.contrib import admin

from .models import MediaImage


class MediaImageAdmin(admin.ModelAdmin):
    list_display = [        
        "title",
        "caption",
        "width",
        "height",
        "kind",
        "spot",
        "created_at",
    ]
    search_fields = ["title", "caption"]


admin.site.register(MediaImage, MediaImageAdmin)
