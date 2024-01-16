import logging

from django.db import models

from .choices import NewsdeskPostStatus

logger = logging.getLogger(__name__)


class NewsdeskPostQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=NewsdeskPostStatus.PUBLISHED)
    
    def get_status_editable(self):
        statuses = [
            NewsdeskPostStatus.ARCHIVED,
            NewsdeskPostStatus.DRAFT,
            NewsdeskPostStatus.HIDDEN,
            NewsdeskPostStatus.PUBLISHED,
            NewsdeskPostStatus.UNPUBLISHED
        ]
        return self.filter(status__in=statuses)

