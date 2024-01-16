from rest_framework import generics, filters

from ...models import Service

from ..serializers import services


class GlobalPresetServiceList(generics.ListAPIView):
    queryset = Service.objects.get_kind_preset_service()
    serializer_class = services.GlobalPresetServiceListSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["title"]
    search_fields = ["title"]
