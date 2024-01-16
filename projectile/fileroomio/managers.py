import logging

from django.db import models

from .choices import FileStatus

logger = logging.getLogger(__name__)


class FileItemQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=FileStatus.PUBLISHED)

    def get_status_editable(self):
        statuses = [
            FileStatus.PUBLISHED,
            FileStatus.DRAFT,
            FileStatus.UNPUBLISHED,
        ]
        return self.filter(status__in=statuses)
