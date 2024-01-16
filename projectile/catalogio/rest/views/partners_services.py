from django.db.models import Q

from rest_framework.generics import get_object_or_404, ListAPIView

from accountio.models import Organization

from catalogio.choices import ServiceKind
from catalogio.models import Service

from weapi.rest.permissions import IsTagConnectorOrganizationStaff
from weapi.rest.serializers.service import PrivateServiceSerializer


class GlobalPartnerServiceList(ListAPIView):
    permission_classes = [IsTagConnectorOrganizationStaff]
    serializer_class = PrivateServiceSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        organization = get_object_or_404(Organization.objects.filter(), slug=slug)

        service_ids = (
            organization.organizationserviceconnector_set.filter().values_list(
                "service_id", flat=True
            )
        )
        return Service.objects.get_status_active().filter(id__in=service_ids)
