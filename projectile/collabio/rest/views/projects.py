from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, filters

from collabio.choices import ProjectStatus, ProjectVisibility
from collabio.models import Project

from mediaroomio.models import MediaImage

from ..serializers import projects


class GlobalProjectList(generics.ListAPIView):
    """Views class for public product list and create"""

    queryset = Project.objects.filter(
        status=ProjectStatus.ACTIVE, visibility=ProjectVisibility.GLOBAL
    )
    serializer_class = projects.GlobalProjectListSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["title", "created_at"]
    search_fields = ["title", "location"]
    filterset_fields = ["country", "location", "phase", "organization__name"]


class GlobalProjectDetail(generics.RetrieveAPIView):
    """Views class for public project detail"""

    queryset = Project.objects.get_visibility_global()
    serializer_class = projects.GlobalProjectDetailSerializer

    def get_object(self):
        kwargs = {"slug": self.kwargs.get("project_slug", None)}
        return get_object_or_404(Project, **kwargs)


class GlobalProjectDetailImageList(generics.ListAPIView):
    """Views class for public project detail"""

    queryset = MediaImage.objects.none()
    serializer_class = projects.GlobalProjectDetailImageSerializer

    def get_queryset(self):
        slug = self.kwargs.get("project_slug")
        project = get_object_or_404(Project.objects.get_visibility_global(), slug=slug)
        ids = project.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        return MediaImage.objects.filter(id__in=ids)
