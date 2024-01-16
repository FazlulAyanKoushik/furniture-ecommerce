from rest_framework import generics
from rest_framework.permissions import AllowAny

from ...models import PotentialLead
from ..serializers.leads import (
    GlobalPotentialLeadSerializer,
)


class PotentialLeadDetail(generics.RetrieveUpdateAPIView):
    queryset = PotentialLead.objects.filter()
    serializer_class = GlobalPotentialLeadSerializer
    lookup_field = "uid"
    permission_classes = [
        AllowAny,
    ]
