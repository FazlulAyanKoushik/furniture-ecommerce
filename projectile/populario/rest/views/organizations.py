from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework.permissions import AllowAny

from populario.models import PopularOrganization
from populario.rest.serializers.organizations import (
    GlobalPopularOrganizationListSerializer,
)


class GlobalPopularOrganizationList(generics.ListAPIView):
    queryset = PopularOrganization.objects.get_popular()[:16]
    serializer_class = GlobalPopularOrganizationListSerializer
    permission_classes = [AllowAny]

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class GlobalPopularOrganizationDetail(generics.RetrieveAPIView):
    queryset = PopularOrganization.objects.filter()
    serializer_class = GlobalPopularOrganizationListSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
