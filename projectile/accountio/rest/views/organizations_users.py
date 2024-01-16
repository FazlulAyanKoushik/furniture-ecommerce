from django.shortcuts import get_object_or_404

from rest_framework import generics

from ...models import OrganizationUser
from ..serializers import organization_users
from ...choices import OrganizationUserStatus
from ..permissions import IsOrganizationStaff


class PublicOrganizationUserList(generics.ListAPIView):
    queryset = OrganizationUser.objects.get_status_active()
    serializer_class = organization_users.PublicOrganizationUserSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        slug = self.kwargs.get("organization_slug", None)
        return self.queryset.filter(organization__slug=slug).select_related("organization")


class PublicOrganizationUserDetail(generics.RetrieveAPIView):
    queryset = OrganizationUser.objects.get_status_active()
    serializer_class = organization_users.PublicOrganizationUserSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "user__slug": self.kwargs.get("slug", None),
        }
        return get_object_or_404(OrganizationUser, **kwargs)
