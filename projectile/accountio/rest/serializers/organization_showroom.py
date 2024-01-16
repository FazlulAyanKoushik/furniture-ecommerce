import logging

from versatileimagefield.serializers import VersatileImageFieldSerializer

from common.serializers import BaseModelSerializer

from mediaroomio.models import MediaImage

logger = logging.getLogger(__name__)


class PublicOrganizationShowroomListSerializer(BaseModelSerializer):
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
            "title",
            "caption",
            "copyright",
            "kind",
        ]

        read_only_fields = [
            "__all__",
        ]
