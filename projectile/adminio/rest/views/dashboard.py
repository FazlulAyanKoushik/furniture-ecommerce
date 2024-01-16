from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters


from accountio.models import Organization

from catalogio.models import Product

from ..permissions import IsStaff
from ..serializers.dashboard import (
    PrivateSalesDashboardSerializer,
    PrivateProductSalesDashboardSerializer,
)


class PrivateSalesDashboard(generics.ListAPIView):
    queryset = Organization.objects.get_status_editable()
    serializer_class = PrivateSalesDashboardSerializer
    permission_classes = [IsStaff]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "country"]
    ordering_fields = ["name", "created_at"]
    filterset_fields = ["country", "status"]


class PrivateProductSalesDashboard(generics.ListAPIView):
    queryset = Product.objects.get_status_editable().select_related(
        "brand", "organization"
    )
    serializer_class = PrivateProductSalesDashboardSerializer
    permission_classes = [IsStaff]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["title", "brand__title"]
    ordering_fields = ["title", "created_at", "updated_at"]
    filterset_fields = ["status", "brand__title", "category"]

    def get_queryset(self):
        queryset = self.queryset
        brand_slugs = self.request.query_params.get("brand", [])
        category_slugs = self.request.query_params.get("category", [])

        if brand_slugs:
            brand_slugs = brand_slugs.split(",")
            queryset = queryset.filter(brand__slug__in=brand_slugs)

        if category_slugs:
            category_slugs = category_slugs.split(",")
            queryset = queryset.filter(category__in=category_slugs)

        return queryset
