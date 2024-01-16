from django.db.models import Q

from django.shortcuts import get_object_or_404
from rest_framework import filters, generics

from accountio.models import Organization
from catalogio.models import Product
from catalogio.choices import ProductChannel

from mediaroomio.models import MediaImage

from ..serializers.organization_products import (
    PublicOrganizationProductListSerializer,
    PublicOrganizationProductDetailSerializer,
    PublicOrganizationProductImageListSerializer,
)


class PublicOrganizationProductList(generics.ListAPIView):
    queryset = Product.objects.get_status_active().select_related(
        "brand", "organization"
    )
    serializer_class = PublicOrganizationProductListSerializer
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
        slug = self.kwargs.get("slug", None)

        # Get active organization slug
        active_organization_slug = self.request.user.get_organization().slug

        organization = get_object_or_404(
            Organization.objects.get_status_fair(), slug=slug
        )
        slugs = list(organization.get_descendants().values_list("slug", flat=True))
        slugs.append(organization.slug)
        # Use default queryset and then chain .filter() to it
        queryset = self.queryset.none()
        if organization.kind == "SUPPLIER":
            if slug == active_organization_slug:
                # Showing products that have channels set to "OWN_CHANNELS" or "ALL_CHANNELS"
                queryset = self.queryset.get_own_channels().filter(organization=organization)
            else:
                # Show products that have channels set to "PARTNERS_CHANNELS" or "ALL_CHANNELS"
                queryset = self.queryset.get_partners_channels().filter(organization__slug__in=slugs)

        elif organization.kind == "RETAILER":
            # Showing products that have channels set to "ALL_CHANNELS" and "PARTIAL_CHANNELS" for retailers
            queryset = self.queryset.get_partners_channels().filter(organization__slug__in=slugs)

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
            color_slugs = color_slugs.split(",")
            queryset = queryset.filter(color__in=color_slugs)

        if material_slugs:
            material_slugs = material_slugs.split(",")
            queryset = queryset.filter(material__in=material_slugs)

        return queryset


class PublicOrganizationProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.get_status_active()
    serializer_class = PublicOrganizationProductDetailSerializer

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "slug": self.kwargs.get("slug", None),
        }
        return get_object_or_404(Product, **kwargs)


class PublicOrganizationProductImageList(generics.ListAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PublicOrganizationProductImageListSerializer

    def get_queryset(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "slug": self.kwargs.get("slug", None),
        }
        product = get_object_or_404(Product.objects.filter(), **kwargs)
        image_ids = product.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        return self.queryset.filter(id__in=image_ids)
