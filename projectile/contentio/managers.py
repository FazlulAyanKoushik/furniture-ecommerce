from django.db import models

from contentio.choices import CustomerServiceStatus


class CustomerServiceQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=CustomerServiceStatus.ACTIVE)

    def get_status_editable(self):
        statuses = [
            CustomerServiceStatus.ACTIVE,
            CustomerServiceStatus.DRAFT,
            CustomerServiceStatus.HIDDEN,
            CustomerServiceStatus.ARCHIVED,
        ]
        return self.filter(status__in=statuses)
