from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response

from accountio.rest.permissions import IsOrganizationStaff

from mediaroomio.choices import MediaImageSpot
from mediaroomio.models import MediaImage, ShowRoomImageConnector

from ..serializers.showroom import (
    PrivateOrganizationShowroomDetailSerializer,
    PrivateOrganizationShowroomListSerializer,
    PrivateShowroomListSerializer,
    PrivateShowroomImageDetailSerializer,
)


class PrivateOrganizationShowroomList(generics.ListCreateAPIView):
    queryset = MediaImage.objects.get_spot_showroom()
    serializer_class = PrivateOrganizationShowroomListSerializer

    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class PrivateOrganizationShowroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_spot_showroom()
    serializer_class = PrivateOrganizationShowroomDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "organization": self.request.user.get_organization(),
            "uid": self.kwargs.get("uid", None),
        }
        return get_object_or_404(self.queryset, **kwargs)


class PrivateShowRoomImageList(generics.ListCreateAPIView):
    serializer_class = PrivateShowroomListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        image = get_object_or_404(MediaImage.objects.get_spot_showroom(), **kwargs)
        gallery_image_ids = image.showroom_image.filter().values_list(
            "gallery_image_id", flat=True
        )

        return {
            "showroom_image": image,
            "gallery_images": MediaImage.objects.get_kind_image().filter(
                id__in=gallery_image_ids
            ),
        }

    def list(self, request, *args, **kwargs):
        serializer = super().get_serializer(self.get_queryset())
        # Code for pagination when pagination feature will available
        # return self.get_paginated_response(serializer.data)
        return Response(data=serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateShowRoomImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateShowroomImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("image_uid", None)
        return generics.get_object_or_404(MediaImage.objects.get_kind_image(), uid=uid)


class PrivateShowRoomCoverImageDetail(generics.UpdateAPIView):
    serializer_class = PrivateShowroomImageDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("image_uid", None)}
        return generics.get_object_or_404(MediaImage.objects.filter(), **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        showroom_uid = self.kwargs.get("uid", None)
        showroom = generics.get_object_or_404(
            MediaImage.objects.get_spot_showroom(), uid=showroom_uid
        )
        instance.image, showroom.image = showroom.image, instance.image
        instance.save()
        showroom.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
