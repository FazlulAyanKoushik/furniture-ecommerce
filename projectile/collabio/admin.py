from django.contrib import admin

from .models import Project, ProjectParticipant


class ProjectParticipantInline(admin.TabularInline):
    model = ProjectParticipant
    extra = 0

    def queryset(self, request):
        return (
            super(ProjectParticipantInline, self)
            .queryset(request)
            .select_related("user")
        )


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "visibility",
        "status",
        "organization",
        "country",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "slug")
    inlines = [
        ProjectParticipantInline,
    ]

    def queryset(self, request):
        return (
            super(ProjectAdmin, self).queryset(request).select_related("organization")
        )


admin.site.register(Project, ProjectAdmin)
