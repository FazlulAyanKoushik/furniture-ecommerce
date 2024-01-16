from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics

from accountio.models import Organization
from catalogio.models import ProductBrand

from ..serializers.organization_products import PublicBrandSlimSerializer


class PublicOrganizationBrandList(generics.ListAPIView):
    queryset = ProductBrand.objects.none()
    serializer_class = PublicBrandSlimSerializer

    def get_queryset(self):
        organization_slug = self.kwargs.get("organization_slug", None)

        organization = get_object_or_404(
            Organization.objects.get_status_fair(), slug=organization_slug
        )

        brands = []
        if organization:
            if organization.kind == "SUPPLIER":
                brands = organization.productbrand_set.filter().order_by("title")
            if organization.kind == "RETAILER":
                # Get all the slugs of the suppliers connected to RETAILER
                slugs = list(organization.get_descendants().values_list("slug", flat=True))
                slugs.append(organization.slug)
                brands = ProductBrand.objects.filter(
                    organization__slug__in=slugs
                ).order_by("title")

        return brands

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
