from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status

from rest_framework.response import Response

from catalogio.rest.permissions import IsOrganizationStaff

from collabio.choices import ProjectStatus
from collabio.models import Project, ProjectParticipant
from collabio.rest.permissions import IsProjectStaff

from fileroomio.models import FileItem

from mediaroomio.models import MediaImage

from ..serializers import projects
from ..serializers.projects import (
    PrivateProjectFileListSerializer,
    PrivateProjectFileDetailSerializer,
    PrivateProjectImageListSerializer,   
    PrivateProjectImageDetailSerializer,
    PrivateProjectListSerializer,
    PrivateProjectDetailSerializer,
    PrivateProjectParticipantListSerializer,
    PrivateProjectParticipantDetailSerializer,
    PrivateProjectCoverImageDetailSerializer
)


class PrivateProjectListView(generics.ListCreateAPIView):
    """View for project list and create"""

    queryset = Project.objects.get_status_editable()
    serializer_class = PrivateProjectListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["country", "location", "phase"]
    ordering_fields = ["title", "created_at"]
    search_fields = ["title"]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View class for project detail"""

    queryset = Project.objects.get_status_editable()
    serializer_class = PrivateProjectDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("project_uid", None)}
        organization = self.request.user.get_organization()
        return get_object_or_404(
            self.queryset.filter(organization=organization), **kwargs
        )

    def perform_destroy(self, instance):
        instance.status = ProjectStatus.REMOVED
        instance.save()


class PrivateProjectParticipantListView(generics.ListCreateAPIView):
    """View for list and create of participants"""

    queryset = ProjectParticipant.objects.filter()
    serializer_class = PrivateProjectParticipantListSerializer
    permission_classes = [IsProjectStaff]

    def get_queryset(self):
        kwargs = {
            "organization": self.request.user.get_organization().id,
            "uid": self.kwargs.get("project_uid"),
        }
        project = generics.get_object_or_404(
            Project.objects.get_status_editable(), **kwargs
        )
        return self.queryset.filter(project=project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_uid"] = self.kwargs.get("project_uid", None)
        return context


class PrivateProjectParticipantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for modification of project participants"""

    queryset = ProjectParticipant.objects.filter()
    serializer_class = PrivateProjectParticipantDetailSerializer
    permission_classes = [IsProjectStaff]
    lookup_field = "uid"

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("participant_uid", None),
            "project__uid": self.kwargs.get("project_uid", None),
        }
        return generics.get_object_or_404(ProjectParticipant.objects.filter(), **kwargs)


class PrivateProjectFileList(generics.ListCreateAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateProjectFileListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        project = generics.get_object_or_404(
            Project.objects.get_status_editable(), **kwargs
        )
        fileitem_ids = project.fileitemconnector_set.filter().values_list(
            "fileitem_id", flat=True
        )
        return self.queryset.filter(id__in=fileitem_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProjectImageList(generics.ListCreateAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = projects.PrivateProjectImageListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        project = generics.get_object_or_404(Project.objects.get_status_active(), uid = uid)
        image_ids = project.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        queryset = self.queryset.filter(id__in=image_ids)
        return queryset
        
       
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        uid = self.kwargs.get("uid", None)
        project = generics.get_object_or_404(Project.objects.get_status_active(), uid = uid)
        cover_image = queryset.filter(image=project.image ).first()
        data = {
                "cover_image": projects.PrivateProjectImageListSerializer(cover_image).data if cover_image else {},
                "images": projects.PrivateProjectImageListSerializer(queryset, many=True).data,
            }
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProjectFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateProjectFileDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("file_uid", None)}
        return generics.get_object_or_404(FileItem.objects.filter(), **kwargs)


class PrivateProjectImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_kind_editable()
    serializer_class = PrivateProjectImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("image_uid", None)}
        return generics.get_object_or_404(MediaImage.objects.filter(), **kwargs)



class PrivateProjectCoverImageDetail(generics.UpdateAPIView):
    serializer_class = PrivateProjectCoverImageDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("image_uid", None)}
        return generics.get_object_or_404(MediaImage.objects.filter(), **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        project_uid = self.kwargs.get("uid", None)
        project = generics.get_object_or_404(
            Project.objects.get_status_active(), uid=project_uid
        )
        project.image = instance.image
        project.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)