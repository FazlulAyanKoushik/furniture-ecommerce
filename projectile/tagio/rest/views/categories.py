from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics

from ...choices import TagCategory
from ...models import Tag
from ..serializers.tags import TagSerializer


class CategoryList(generics.ListAPIView):
    queryset = Tag.objects.filter(category=TagCategory.PRODUCT, parent__isnull=True)
    serializer_class = TagSerializer

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
