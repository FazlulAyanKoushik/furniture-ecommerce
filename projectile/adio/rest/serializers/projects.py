from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from adio.models import AdProject

from weapi.rest.serializers.ads import PrivateProjectAdSlimSerializer


class GlobalProjectAdSerializer(serializers.ModelSerializer):
    project = PrivateProjectAdSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = AdProject
        fields = [
            "slug",
            "project",
            "organization",
            "start_date",
            "stop_date",
            "status",
            "view_count",
            "click_count",
        ]
        read_only_fields = ["__all__"]
