from django.shortcuts import get_object_or_404

from rest_framework import generics

from accountio.rest.permissions import IsOrganizationStaff

from gruppio.models import Group
from gruppio.choices import GroupStatus

from ..serializers import organizations_group


class PublicOrganizationGroupList(generics.ListAPIView):
    """List view for Organization Group"""

    queryset = Group.objects.get_status_active()
    serializer_class = organizations_group.PublicOrganizationGroupListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)
        return self.queryset.filter(organization__slug=slug).select_related(
            "organization"
        )


class PublicOrganizationGroupDetail(generics.RetrieveAPIView):
    """Detail view for Organization Group"""

    queryset = Group.objects.get_status_active()
    serializer_class = organizations_group.PublicOrganizationGroupDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "slug": self.kwargs.get("group_slug", None),
        }
        return get_object_or_404(Group, **kwargs)
