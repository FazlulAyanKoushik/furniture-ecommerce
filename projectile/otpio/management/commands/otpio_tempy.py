from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...models import UserPhoneOTP


class Command(BaseCommand):
    help = "Otp's will be removed every 4 hours."

    def handle(self, *args, **options):

        # Define the timeout threshold for OTPs (in minutes)
        timeout_minute = 1

        # Calculate the timestamp of the timeout threshold
        timeout_threshold = timezone.now() - timedelta(minutes=timeout_minute)

        # Delete all expired OTPs from the database
        expired_otps = UserPhoneOTP.objects.filter(created_at__lt=timeout_threshold)
        expired_otps.delete()
