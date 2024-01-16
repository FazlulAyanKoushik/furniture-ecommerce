from django.shortcuts import get_object_or_404

from rest_framework import generics

from mediaroomio.models import MediaImage, MediaImageConnector

from ..serializers.organizations_images import (
    PublicImageListSerializer,
    PublicImageDetailSerializer,
)


class PublicImageList(generics.ListAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PublicImageListSerializer

    def get_queryset(self):
        slug = self.kwargs.get("organization_slug")
        image_ids = MediaImageConnector.objects.filter(
            organization_slug=slug
        ).values_list("image_id", flat=True)
        return self.queryset.filter(id__in=image_ids)


class PublicImageDetail(generics.RetrieveAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PublicImageDetailSerializer

    def get_object(self):
        kwargs = {
            "organization_slug": self.kwargs.get("organization_slug", None),
            "uid": self.kwargs.get("image_uid", None),
        }

        return get_object_or_404(MediaImage, **kwargs)
