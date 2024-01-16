from django.shortcuts import get_object_or_404
from rest_framework import generics

from catalogio.rest.permissions import IsOrganizationStaff

from newsdeskio.models import NewsdeskPost
from newsdeskio.choices import NewsdeskPostStatus

from ..serializers.organization_news import (
    PublicOrganizationNewsListSerializer,
    PublicOrganizationNewsDetailSerializer,
)


class PublicOrganizationNewsList(generics.ListAPIView):
    """View for creating and returning list of news of organization"""

    queryset = NewsdeskPost.objects.get_status_active()
    serializer_class = PublicOrganizationNewsListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        slug = self.kwargs.get("organization_slug", None)
        return self.queryset.filter(organization__slug=slug)


class PublicOrganizationNewsDetail(generics.RetrieveAPIView):
    """Detail view for organization news"""

    queryset = NewsdeskPost.objects.get_status_active()
    serializer_class = PublicOrganizationNewsDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "slug": self.kwargs.get("post_slug", None),
        }
        return get_object_or_404(NewsdeskPost, **kwargs)
