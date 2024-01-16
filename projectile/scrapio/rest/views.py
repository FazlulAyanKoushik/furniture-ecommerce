from rest_framework import generics

from common.paginators import TwoThousandResultsSetPagination

from ..models import ScrapProductData

from .serializers import ScrapProductDataSerializer


class ScrapedProductList(generics.ListAPIView):
    queryset = ScrapProductData.objects.filter()
    serializer_class = ScrapProductDataSerializer
    pagination_class = TwoThousandResultsSetPagination
    permission_classes = []
