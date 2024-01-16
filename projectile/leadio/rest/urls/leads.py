from django.urls import path

from ..views.leads import PotentialLeadDetail

urlpatterns = [
    path(
        r"/<uuid:uid>", PotentialLeadDetail.as_view(), name="leads.potentiallead-detail"
    ),
]
