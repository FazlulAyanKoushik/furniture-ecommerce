from django.db import models

from .choices import TagStatus, TagCategory


class TagQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=TagStatus.ACTIVE)

    def get_status_fair(self):
        tag_category = [TagCategory.PRESET_SERVICE, TagCategory.SERVICE]
        return self.filter(status=TagStatus.ACTIVE, category__in=tag_category)
