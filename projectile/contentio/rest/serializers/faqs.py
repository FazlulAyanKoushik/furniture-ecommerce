from rest_framework import serializers

from contentio.models import FAQ

from versatileimagefield.serializers import VersatileImageFieldSerializer


class GlobalFAQSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "crop__512x512"),
            ("at256", "crop__256x256"),
        ],
        required=False,
    )

    class Meta:
        model = FAQ
        fields = [
            "title",
            "slug",
            "category",
            "image",
            "youtube_url",
            "content",
            "summary",
        ]

        read_only_fields = ["__all__"]
