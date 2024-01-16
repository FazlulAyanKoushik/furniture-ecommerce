from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization


class PrivateSelfOrganizationListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
            ("at128", "thumbnail__128x128"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "uid",
            "slug",
            "name",
            "city",
            "country",
            "email",
            "phone",
            "website_url",
            "summary",
            "description",
            "status",
            "avatar",
            "hero",
            "logo_wide",
            "image",
            "kind",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["__all__"]
    
    def get_name(self, instance):
        return instance.display_name or instance.name


class PrivateOrganizationSlimSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x400", "crop__400x400"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "uid",
            "slug",
            "name",            
            "email",
            "phone",
            "registration_no",
            "summary",
            "description",
            "image",
            "kind",
            "size",
            "website_url",
            "city",
            "country",
        ]
        read_only_fields = ["__all__"]
    
    def get_name(self, instance):
        return instance.display_name or instance.name
