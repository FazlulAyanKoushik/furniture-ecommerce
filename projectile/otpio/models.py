import datetime

import logging

from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import BaseModelWithUID

from .choices import UserPhoneStatus, UserPhoneOTPStatus

from .managers import UserPhoneQuerySet

logger = logging.getLogger(__name__)


class UserPhone(BaseModelWithUID):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, unique=True)

    status = models.CharField(
        max_length=20,
        choices=UserPhoneStatus.choices,
        db_index=True,
        default=UserPhoneStatus.PENDING,
    )

    is_primary = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(default="127.0.0.1")

    objects = UserPhoneQuerySet.as_manager()

    def __str__(self):
        return f"ID: {self.id}, User: {self.user}, Phone: {self.phone}"

    def make_primary(self):
        self.is_primary = True
        self.save_dirty_fields()

    def is_status_active(self):
        self.status = UserPhoneStatus.ACTIVE
        self.save_dirty_fields()

    def save(self, *args, **kwargs):
        if self.is_primary:
            self.user.userphone_set.filter(is_primary=True).exclude(id=self.id).update(
                is_primary=False
            )
        super().save(*args, **kwargs)


class UserPhoneOTP(models.Model):

    phone = models.ForeignKey(
        UserPhone, on_delete=models.CASCADE
    )
    otp = models.CharField(max_length=6)
    status = models.CharField(
        max_length=20,
        choices=UserPhoneOTPStatus.choices,
        db_index=True,
        default=UserPhoneOTPStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id}, User: {self.phone.user}, Otp: {self.otp}"

    def is_expired(self):
        """Returns True if the OTP code has expired, False otherwise."""
        return self.created_at < timezone.now()
    
    def is_status_consumed(self):
        self.status = UserPhoneOTPStatus.CONSUMED
        self.save_dirty_fields()

    def save(self, *args, **kwargs):
        self.created_at = datetime.datetime.now() + datetime.timedelta(seconds=60)
        super().save(*args, **kwargs)

   