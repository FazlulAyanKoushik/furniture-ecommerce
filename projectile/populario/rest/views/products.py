from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework.permissions import AllowAny

from common.paginators import RestricedResultsSetPagination

from catalogio.models import Product

from populario.rest.serializers.products import GlobalPopularProductSerializer


class GlobalPopularProductList(generics.ListAPIView):
    queryset = Product.objects.get_status_active().order_by("-view_count")
    serializer_class = GlobalPopularProductSerializer
    pagination_class = RestricedResultsSetPagination
    permission_classes = [AllowAny]

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
