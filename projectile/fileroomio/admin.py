from django.contrib import admin

from .models import FileItem, FileItemAccess, FileItemConnector


class FileItemAccessInline(admin.TabularInline):
    model = FileItemAccess
    extra = 1


class FileItemAdmin(admin.ModelAdmin):
    list_display = ["name", "kind", "status", "organization", "created_at"]
    search_fields = ["name", "status"]
    inlines = [FileItemAccessInline]


class FileItemAccessAdmin(admin.ModelAdmin):
    list_display = ["fileitem", "partner", "user", "kind"]


admin.site.register(FileItem, FileItemAdmin)
admin.site.register(FileItemConnector)
admin.site.register(FileItemAccess, FileItemAccessAdmin)
