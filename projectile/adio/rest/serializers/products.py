from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from adio.models import AdProduct

from weapi.rest.serializers.ads import PrivateProductAdSlimSerializer


class GlobalProductAdSerializer(serializers.ModelSerializer):
    product = PrivateProductAdSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = AdProduct
        fields = [
            "slug",
            "product",
            "organization",
            "start_date",
            "stop_date",
            "status",
            "view_count",
            "click_count",
        ]
        read_only_fields = ["__all__"]
