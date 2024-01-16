from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)

from catalogio.choices import ServiceKind, ServiceStatus
from catalogio.models import Service, OrganizationServiceConnector

from weapi.rest.permissions import IsOrganizationServiceConnectorStaff

from ..serializers.service import PrivateServiceSerializer


class PrivateServiceList(ListCreateAPIView):
    serializer_class = PrivateServiceSerializer
    permission_classes = [IsOrganizationServiceConnectorStaff]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title"]
    ordering_fields = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        service_ids = (
            organization.organizationserviceconnector_set.filter().values_list(
                "service_id", flat=True
            )
        )
        return Service.objects.get_status_active().filter(id__in=service_ids)


class PrivateServiceDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateServiceSerializer
    permission_classes = [IsOrganizationServiceConnectorStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        queryset = Service.objects.get_status_active()
        return get_object_or_404(queryset.filter(), uid=uid)

    def perform_destroy(self, instance):
        instance.status = ServiceStatus.REMOVED
        instance.save()

