from rest_framework import generics
from rest_framework.permissions import AllowAny

from accountio.models import OrganizationUser
from accountio.rest.serializers.organizations import (
    PublicOrganizationUserInviteSerializer,
)


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = OrganizationUser.objects.get_status_editable()
    serializer_class = PublicOrganizationUserInviteSerializer
    permission_classes = [AllowAny]
    lookup_field = "token"
