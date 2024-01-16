from django.db import models

from .choices import SubscriptionPlanStatus, SubscriptionSessionStatus


class SubscriptionPlanQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=SubscriptionPlanStatus.PUBLISHED)

    def get_status_editable(self):
        statuses = [
            SubscriptionPlanStatus.DRAFT,
            SubscriptionPlanStatus.PUBLISHED,
            SubscriptionPlanStatus.ARCHIVED,
            SubscriptionPlanStatus.HIDDEN,
        ]
        return self.filter(status__in=statuses)


class SubscriptionSessionQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=SubscriptionSessionStatus.ACTIVE)
