from django.db import models


class PotentialLeadStatus(models.TextChoices):
    UNTOUCHED = "UNTOUCHED", "Untouched"
    CONTACTED = "CONTACTED", "Contacted"
    UNAVAILABLE = "UNAVAILABLE", "Unavailable"
    WRONG_NUMBER = "WRONG_NUMBER", "Wrong Number"
    NOT_INTERESTED = "NOT_INTERESTED", "Not Interested"
    INTERESTED = "INTERESTED", "Interested"
    FOLLOW_UP = "FOLLOW_UP", "Follow Up"
    CLOSED = "CLOSED", "Closed"
