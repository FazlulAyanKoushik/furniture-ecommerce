from django.shortcuts import get_object_or_404

from rest_framework import generics

from accountio.rest.permissions import IsOrganizationStaff

from mediaroomio.models import MediaImage, MediaImageConnector

from ..serializers.mediaroom import (
    PrivateGroupImageSerializer,
    PrivateOrganizationImageListSerializer,
    PrivateOrganizationImageDetailSerializer,
    PrivateProductImageSerializer,
    PrivateProjectImageSerializer,
)


class PrivateOrganizationImageList(generics.ListAPIView):
    queryset = MediaImage.objects.get_kind_editable()
    serializer_class = PrivateOrganizationImageListSerializer

    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateOrganizationImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_kind_editable()
    serializer_class = PrivateOrganizationImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization": self.request.user.get_organization(),
            "uid": self.kwargs.get("uid", None),
        }

        return get_object_or_404(MediaImage.objects.filter(), **kwargs)


class PrivateGroupImageList(generics.ListCreateAPIView):
    queryset = MediaImageConnector.objects.get_kind_group()
    serializer_class = PrivateGroupImageSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        return self.queryset.filter(group__uid=uid)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProductImageList(generics.ListCreateAPIView):
    queryset = MediaImageConnector.objects.get_kind_product()
    serializer_class = PrivateProductImageSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        return self.queryset.filter(product__uid=uid)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProjectImageList(generics.ListCreateAPIView):
    queryset = MediaImageConnector.objects.get_kind_project()
    serializer_class = PrivateProjectImageSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        return self.queryset.filter(project__uid=uid)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context
