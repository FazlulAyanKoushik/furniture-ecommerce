import logging

from django.db import transaction


logger = logging.getLogger(__name__)


@transaction.atomic
def post_save_member(sender, instance, created, **kwargs):
    if created:
        pass


@transaction.atomic
def post_delete_member(sender, instance, *args, **kwargs):
    pass
