from rest_framework import serializers

from populario.models import PopularOrganization
from populario.rest.serializers.products import GlobalOrganizationSlimSerializer


class GlobalPopularOrganizationListSerializer(serializers.ModelSerializer):
    organization = GlobalOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = PopularOrganization
        fields = ["slug", "organization", "status"]
        read_only_fields = ["__all__"]
