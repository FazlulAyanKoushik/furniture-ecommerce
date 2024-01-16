from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics

from ...models import ProductBrand

from ..serializers import brands


class GlobalBrandList(generics.ListAPIView):
    queryset = (
        ProductBrand.objects.filter().select_related("organization").order_by("title")
    )
    serializer_class = brands.GlobalProductBrandSerializer

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
