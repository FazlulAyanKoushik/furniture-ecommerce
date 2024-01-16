from django.contrib import admin

from .models import Group, Member


class MemberInline(admin.TabularInline):
    model = Member
    extra = 0
    readonly_fields = ("referrer",)

    def queryset(self, request):
        return (
            super(MemberInline, self)
            .queryset(request)
            .select_related("user", "referrer")
        )


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "kind",
        "country",
        "post_count",
        "member_count",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)
    inlines = [
        MemberInline,
    ]

    def queryset(self, request):
        return super(GroupAdmin, self).queryset(request).select_related("organization")


admin.site.register(Group, GroupAdmin)

admin.site.register(Member)
