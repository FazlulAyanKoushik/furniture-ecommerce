from rest_framework import generics

from accountio.rest.permissions import IsOrganizationStaff

from mediaroomio.models import MediaImage

from ..serializers.organization_showroom import (
    PublicOrganizationShowroomListSerializer,
)


class PublicOrganizationShowroomList(generics.ListAPIView):
    queryset = MediaImage.objects.get_spot_showroom()
    serializer_class = PublicOrganizationShowroomListSerializer

    def get_queryset(self):
        organization_slug = self.kwargs["organization_slug"]
        return self.queryset.filter(organization_slug=organization_slug)
