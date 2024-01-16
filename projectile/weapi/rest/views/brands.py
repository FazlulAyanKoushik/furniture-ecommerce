from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from rest_framework.exceptions import PermissionDenied

from accountio.rest.permissions import IsOrganizationStaff
from catalogio.models import ProductBrand

from ..serializers.brands import (
    PrivateProductBrandListSerializer,
    PrivateProductBrandDetailSerializer,
)


class PrivateOrganizationProductBrandList(generics.ListCreateAPIView):
    queryset = ProductBrand.objects.filter()
    serializer_class = PrivateProductBrandListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        user_organization = self.request.user.get_organization()
        return self.queryset.filter(organization=user_organization)


class PrivateOrganizationProductBrandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductBrand.objects.filter()
    serializer_class = PrivateProductBrandDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization": self.request.user.get_organization(),
            "uid": self.kwargs.get("uid", None),
        }

        return get_object_or_404(ProductBrand, **kwargs)

    def perform_destroy(self, instance):
        if instance.product_set.exists():
            raise PermissionDenied(
                {
                    "detail": "Brand has connected products, Please remove product(s) first!"
                }
            )
        return super().perform_destroy(instance)
