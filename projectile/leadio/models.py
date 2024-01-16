from django.db import models

from simple_history.models import HistoricalRecords

from common.lists import COUNTRIES
from common.models import BaseModelWithUID

from .choices import PotentialLeadStatus


class PotentialLead(BaseModelWithUID):
    name = models.CharField(max_length=100)
    organization_no = models.CharField(max_length=40, blank=True)
    address = models.TextField(blank=True)
    postal_code = models.CharField(max_length=40, blank=True)
    postal_area = models.CharField(max_length=40, blank=True)
    country = models.CharField(max_length=40)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    source_url = models.URLField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=PotentialLeadStatus.choices,
        default=PotentialLeadStatus.UNTOUCHED,
    )

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"Title: {self.name}, Country: ({self.country})"


class LeadContact(BaseModelWithUID):
    lead = models.ForeignKey(PotentialLead, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return f"Name: {self.get_full_name()} , Phone: ({self.phone})"

    def get_full_name(self) -> str:
        return " ".join([self.first_name, self.last_name])
