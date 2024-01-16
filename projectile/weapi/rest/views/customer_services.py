from rest_framework import generics

from contentio.models import CustomerService

from catalogio.rest.permissions import IsOrganizationStaff

from ..serializers.customer_services import PrivateCustomerServiceSerializer


class PrivateCustomerServiceList(generics.ListCreateAPIView):
    queryset = CustomerService.objects.get_status_editable()
    serializer_class = PrivateCustomerServiceSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.get_organization())

    def perform_create(self, serializer):
        organization = self.request.user.get_organization()
        serializer.save(organization=organization)


class PrivateCustomerServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerService.objects.get_status_editable()
    serializer_class = PrivateCustomerServiceSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("uid", None),
        }
        return generics.get_object_or_404(self.queryset.filter(), **kwargs)
