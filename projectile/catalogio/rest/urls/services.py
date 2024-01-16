from django.urls import path

from ..views import services

urlpatterns=[
    path(r"", services.GlobalPresetServiceList.as_view(), name="services.preset_services-list"),
]
