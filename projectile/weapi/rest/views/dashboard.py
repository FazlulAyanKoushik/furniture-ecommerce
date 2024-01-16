from rest_framework.response import Response
from rest_framework.views import APIView

from accountio.models import (
    OrganizationUser,
)
from catalogio.models import Product, Service


class WeDashboard(APIView):
    def get(self, request, format=None):
        try:
            organization = request.user.get_organization()
            partners = organization.get_descendants()

            product_count = (
                Product.objects.get_status_active()
                .filter(organization=organization)
                .count()
            )

            partner_count = partners.count()
            user_count = (
                OrganizationUser.objects.get_status_active()
                .filter(organization=organization)
                .count()
            )
            service_ids = organization.organizationserviceconnector_set.filter().values_list(
                "service_id", flat=True
            )
            service_count = Service.objects.get_status_active().filter(id__in=service_ids).count()
            return Response(
                {
                    "product_count": product_count,
                    "partner_count": partner_count,
                    "user_count": user_count,
                    "service_count": service_count,
                }
            )

        except AttributeError:
            return Response(
                {
                    "message": "Organization with default permissions not found.",
                }
            )
