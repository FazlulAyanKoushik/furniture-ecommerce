from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from core.models import User

from newsdeskio.models import NewsdeskPost


class PublicAuthorSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "slug",
            "first_name",
            "last_name",
            "email",
            "status",
        ]
        read_only_fields = ["__all__"]


class PublicOrganizationNewsListSerializer(serializers.ModelSerializer):
    author = PublicAuthorSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = NewsdeskPost
        fields = [
            "slug",
            "title",
            "summary",
            "description",
            "image",
            "organization",
            "kind",
            "status",
            "author",
            "is_featured",
            "created_at",
        ]
        read_only_fields = ("__all__",)

    def create(self, validated_data):
        return NewsdeskPost.objects.create(
            author=self.context["request"].user,
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )


class PublicOrganizationNewsDetailSerializer(serializers.ModelSerializer):
    author = PublicAuthorSlimSerializer(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = NewsdeskPost
        fields = [
            "title",
            "summary",
            "description",
            "image",
            "organization",
            "kind",
            "status",
            "author",
            "is_featured",
            "created_at",
        ]
        read_only_fields = ("__all__",)
