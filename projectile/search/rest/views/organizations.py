from rest_framework import filters, generics

from django_filters.rest_framework import DjangoFilterBackend

from accountio.models import Organization
from accountio.rest.serializers import organizations


class SearchOrganizationList(generics.ListAPIView):
    queryset = Organization.objects.get_status_fair().order_by("name")
    serializer_class = organizations.PublicOrganizationListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "kind",
        "segment",
        "postal_area",
        "city",
        "country",
        "tagconnector__tag__name",
    ]
    search_fields = ["^name", "^display_name"]

    def get_queryset(self):
        categories = self.request.query_params.get("categories", None)
        queryset = self.queryset
        if categories is not None:
            queryset = self.queryset.filter(
                categories__contains=[{"value": categories}]
            )
        return queryset
