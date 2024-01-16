from django.shortcuts import get_object_or_404

from rest_framework import generics

from collabio.choices import ProjectStatus
from collabio.models import Project

from collabio.rest.serializers import projects


class PublicOrganizationProjectList(generics.ListAPIView):
    """Views class for public product list and create"""

    queryset = Project.objects.get_status_active()
    serializer_class = projects.GlobalProjectListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("organization_slug", None)
        return self.queryset.filter(organization__slug=slug)


class PublicOrganizationProjectDetail(generics.RetrieveAPIView):
    """Views class for public project detail"""

    queryset = Project.objects.get_status_active()
    serializer_class = projects.GlobalProjectDetailSerializer

    def get_object(self):
        kwargs = {
            "organization__slug": self.kwargs.get("organization_slug", None),
            "slug": self.kwargs.get("project_slug", None),
        }
        return get_object_or_404(Project, **kwargs)
