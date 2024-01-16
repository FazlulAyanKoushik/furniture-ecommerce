from django.contrib import admin

from .models import UserPhoneOTP, UserPhone

# Register your models here.
admin.site.register(UserPhone)
admin.site.register(UserPhoneOTP)