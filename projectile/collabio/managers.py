import logging

from django.db import models

from .choices import ProjectStatus, ProjectVisibility

logger = logging.getLogger(__name__)


class ProjectQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=ProjectStatus.ACTIVE)

    def get_visibility_global(self):
        return self.get_status_active().filter(visibility=ProjectVisibility.GLOBAL)

    def get_popular(self):
        return self.get_visibility_global().exclude(image="").order_by("?")

    def get_status_editable(self):
        statues = [
            ProjectStatus.ACTIVE,
            ProjectStatus.ARCHIVED,
            ProjectStatus.DRAFT,
            ProjectStatus.HIDDEN,
        ]
        return self.filter(status__in=statues)
