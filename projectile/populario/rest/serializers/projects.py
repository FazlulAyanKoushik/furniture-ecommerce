from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from collabio.models import Project

from common.serializers import BaseModelSerializer

from populario.models import PopularProject
from populario.rest.serializers.products import GlobalOrganizationSlimSerializer


class GlobalProjectSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "slug",
            "title",
            "image",
            "location",
            "country",
        ]
        read_only_fields = ["__all__"]


class GlobalPopularProjectSerializer(BaseModelSerializer):
    organization = GlobalOrganizationSlimSerializer(read_only=True)
    project = GlobalProjectSlimSerializer(read_only=True)

    class Meta:
        model = PopularProject
        fields = ["slug", "project", "organization", "status"]
        read_only_fields = ["__all__"]
