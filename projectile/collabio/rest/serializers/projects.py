from rest_framework.serializers import ModelSerializer

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from collabio.models import Project

from mediaroomio.models import MediaImage


class GlobalProjectListSerializer(ModelSerializer):
    """Serializer class for Project"""

    organization = PublicOrganizationSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "uid",
            "slug",
            "title",
            "location",
            "phase",
            "country",
            "image",
            "organization",
        ]


class GlobalProjectDetailSerializer(ModelSerializer):
    """Serializer class for Project"""

    organization = PublicOrganizationSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "thumbnail__400x400"),
            ("at800", "thumbnail__800x800"),
        ],
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "summary",
            "description",
            "location",
            "country",
            "phase",
            "image",
            "organization",
        ]


class GlobalProjectDetailImageSerializer(ModelSerializer):

    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "thumbnail__400x400"),
            ("at800", "thumbnail__800x800"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "image",
        ]
