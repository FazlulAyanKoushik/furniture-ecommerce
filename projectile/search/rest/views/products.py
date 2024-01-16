from rest_framework import filters, generics

from catalogio.models import Product
from catalogio.rest.serializers import products

from tagio.choices import TagCategory, TagEntity
from tagio.models import TagConnector


class GlobalProductSearchList(generics.ListAPIView):
    queryset = Product.objects.get_status_active().select_related(
        "brand", "organization"
    )
    serializer_class = products.GlobalProductListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    search_fields = [
        "title",
        "description",
        "display_title",
        "organization__name",
        "brand__title",
    ]

    ordering_fields = ["title", "created_at"]

    def get_queryset(self):
        queryset = self.queryset
        brand_slugs = self.request.query_params.get("brand", None)
        category_slugs = self.request.query_params.get("category", None)
        color_slugs = self.request.query_params.get("color", None)
        material_slugs = self.request.query_params.get("material", None)

        if brand_slugs:
            brand_slugs = brand_slugs.split(",")
            queryset = queryset.filter(brand__slug__in=brand_slugs)

        if category_slugs:
            category_slugs = category_slugs.split(",")
            queryset = queryset.filter(category__in=category_slugs)

        if color_slugs:
            # tag_connectors = TagConnector.objects.filter(
            #     tag__slug__in=color_slugs , entity=TagEntity.PRODUCT
            # )
            # tags = tag_connectors.filter(tag__category=TagCategory.COLOR)
            # product_ids = set(tags.values_list("product_id", flat=True))
            color_slugs = color_slugs.split(",")
            queryset = queryset.filter(color__in=color_slugs)

        if material_slugs:
            # tag_connectors = TagConnector.objects.filter(
            #     tag__slug__in=material_slugs , entity=TagEntity.PRODUCT
            # )
            # tags = tag_connectors.filter(tag__category=TagCategory.MATERIAL)
            # product_ids = set(tags.values_list("product_id", flat=True))
            material_slugs = material_slugs.split(",")
            queryset = queryset.filter(material__in=material_slugs)

        return queryset
