from rest_framework import generics
from rest_framework.permissions import AllowAny

from adio.models import AdOrganization
from ..serializers.organizations import GlobalOrganizationAdSerializer


class GlobalOrganizationAdList(generics.ListAPIView):
    queryset = AdOrganization.objects.get_status_active().order_by("?")[:4]
    serializer_class = GlobalOrganizationAdSerializer
    permission_classes = [AllowAny]


class GlobalOrganizationAdDetail(generics.RetrieveAPIView):
    serializer_class = GlobalOrganizationAdSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        ad_organization = generics.get_object_or_404(
            AdOrganization.objects.get_status_active(), slug=slug
        )
        ad_organization.increment_count()
        return ad_organization
