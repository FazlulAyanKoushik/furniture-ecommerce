import csv
import os
import sys

from django.core.management.base import BaseCommand

from core.emails import send_generic_invite_mail
from core.models import User, Organization, OrganizationUser

from groupio.choices import MemberStatus
from groupio.models import Group, Member


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        pass
