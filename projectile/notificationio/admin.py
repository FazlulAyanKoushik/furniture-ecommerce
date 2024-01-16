from django.contrib import admin
from .models import Notification, NotificationSettings

# Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationSettings)
