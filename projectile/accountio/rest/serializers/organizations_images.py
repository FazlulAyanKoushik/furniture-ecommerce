from versatileimagefield.serializers import VersatileImageFieldSerializer

from mediaroomio.models import MediaImage

from common.serializers import BaseModelSerializer


class PublicImageListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "uid",
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
            "kind",
        ]
        read_only_fields = ("__all__",)


class PublicImageDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
            "kind",
        ]
        read_only_fields = ("__all__",)
