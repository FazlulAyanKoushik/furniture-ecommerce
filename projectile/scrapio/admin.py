from django.contrib import admin

from . import models


class ScrapAdmin(admin.ModelAdmin):
    list_display = ["id", "organization", "category", "title", "created_at"]
    list_filter = ["organization", "category", "created_at"]


admin.site.register(models.ScrapProductData, ScrapAdmin)
