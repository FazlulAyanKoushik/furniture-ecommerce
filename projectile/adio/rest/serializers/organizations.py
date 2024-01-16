from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from adio.models import AdOrganization


class GlobalOrganizationAdSerializer(serializers.ModelSerializer):
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = AdOrganization
        fields = [
            "slug",
            "organization",
            "start_date",
            "stop_date",
            "status",
            "view_count",
            "click_count",
        ]
        read_only_fields = ["__all__"]
