from rest_framework import generics
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from accountio.models import Organization
from accountio.rest.serializers.organizations import PublicOrganizationListSerializer


class PrivateOrganizationSearchList(generics.ListAPIView):
    queryset = Organization.objects.none()
    serializer_class = PublicOrganizationListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "country",
    ]
    search_fields = [
        "name",
        "display_name",
        "postal_area",
        "city",
    ]

    def get_queryset(self):
        request = self.request
        organization = request.user.get_organization()
        return organization.get_descendants()
