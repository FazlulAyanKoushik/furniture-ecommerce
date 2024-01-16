import logging


from accountio.models import Organization
from common.serializers import BaseModelSerializer


logger = logging.getLogger(__name__)


class PrivateWeStatusSerializer(BaseModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "status",
        ]
