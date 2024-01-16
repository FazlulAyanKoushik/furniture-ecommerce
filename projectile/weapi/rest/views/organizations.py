from rest_framework import generics

from accountio.models import Organization
from accountio.rest.permissions import IsOrganizationStaff

from ..serializers.organizations import (
    PrivateSelfOrganizationListSerializer,
)


class PrivateSelfOrganzationList(generics.ListAPIView):
    queryset = Organization.objects.get_status_editable()
    serializer_class = PrivateSelfOrganizationListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        user = self.request.user
        ids = user.profiles.filter().values_list("organization_id", flat=True)
        return self.queryset.filter(id__in=ids)
