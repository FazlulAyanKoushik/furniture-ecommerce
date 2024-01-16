from rest_framework import generics, filters
from rest_framework.generics import get_object_or_404

from catalogio.choices import ProductMaterialStatus
from catalogio.models import Material
from catalogio.rest.permissions import IsOrganizationStaff

from ..serializers.materials import (
    PrivateMaterialSerializer,
)


class PrivateMaterialList(generics.ListCreateAPIView):
    serializer_class = PrivateMaterialSerializer
    queryset = Material.objects.get_status_editable()
    permission_classes = [IsOrganizationStaff]

    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ["name"]

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.get_organization())


class PrivateMaterialDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateMaterialSerializer
    queryset = Material.objects.get_status_editable()
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        return get_object_or_404(Material.objects.filter(), uid=uid)

    def perform_destroy(self, instance):
        instance.status = ProductMaterialStatus.REMOVED
        instance.save()