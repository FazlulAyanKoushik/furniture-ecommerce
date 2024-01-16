from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny

from adio.models import AdProduct

from ..serializers.products import GlobalProductAdSerializer


class GlobalProductAdsList(generics.ListAPIView):
    queryset = AdProduct.objects.get_status_active().order_by("?")[:4]
    serializer_class = GlobalProductAdSerializer
    permission_classes = [AllowAny]


class GlobalProductAdDetail(generics.RetrieveAPIView):
    serializer_class = GlobalProductAdSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        ad_product = get_object_or_404(AdProduct.objects.get_status_active(), slug=slug)
        ad_product.increment_count()
        return ad_product
