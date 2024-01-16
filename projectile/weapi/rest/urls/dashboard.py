
from django.urls import path
from ..views.dashboard import WeDashboard

urlpatterns = [
    path(
        r"", 
        WeDashboard.as_view(),
        name="wedashboard-detail"
    ),
]