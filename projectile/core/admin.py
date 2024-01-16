from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, UserEmail


class UserEmailInline(admin.TabularInline):
    model = UserEmail
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [        
        "email",
        "first_name",
        "last_name",
        "slug",
        "phone",
        "is_active",
        "status",
        "gender",
        "objective",
        "date_joined",
        "last_login",
    ]
    list_filter = UserAdmin.list_filter + ("status",)
    ordering = ("-date_joined",)
    inlines = (UserEmailInline,)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {
                "fields": (
                    "phone",
                    "headline",
                    "avatar",
                    "hero",
                    "gender",
                    "status",
                    "objective",
                    "date_of_birth",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),
    ) + UserAdmin.add_fieldsets
