from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics

from accountio.rest.permissions import IsOrganizationStaff

from invitio.choices import OrganizationInviteResponse
from invitio.models import OrganizationInvite

from ..serializers import invites


class PrivateOutgoingInviteList(generics.ListAPIView):
    serializer_class = invites.PrivatePartnerOutgoingInviteSerializer
    queryset = OrganizationInvite.objects.filter()
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["response"]
    search_fields = ["target__name"]

    def get_queryset(self):
        return self.queryset.filter(
            organization=self.request.user.get_organization(),
            response=OrganizationInviteResponse.PENDING,
        )


class PrivateInviteResponseDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = invites.PrivateInviteResponseSerializer

    def get_object(self):
        kwargs = {"token": self.kwargs.get("token", None)}
        return generics.get_object_or_404(
            OrganizationInvite.objects.filter(),
            target=self.request.user.get_organization(),
            response=OrganizationInviteResponse.PENDING,
            **kwargs
        )


class PrivateIncomingInviteList(generics.ListAPIView):
    queryset = OrganizationInvite.objects.filter()
    permission_classes = [IsOrganizationStaff]
    serializer_class = invites.PrivatePartnerIncomingInviteSerializer
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["response"]
    search_fields = ["organization__name"]

    def get_queryset(self):
        return self.queryset.filter(
            target=self.request.user.get_organization(),
            response=OrganizationInviteResponse.PENDING,
        )
