from rest_framework import serializers

from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from catalogio.models import Material

from versatileimagefield.serializers import VersatileImageFieldSerializer



class PrivateMaterialSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)
   

    class Meta:
        model = Material
        fields = [
            "uid",
            "slug",
            "name",
            "description",
            "status",
            "image",
            "organization",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "category", "created_at", "updated_at"]

    def create(self, validated_data):
        organization = self.context["request"].user.get_organization()
        return Material.objects.create(organization=organization, **validated_data)
