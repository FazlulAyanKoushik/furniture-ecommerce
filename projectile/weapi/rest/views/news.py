from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics
from rest_framework.response import Response

from accountio.models import Organization

from catalogio.rest.permissions import IsOrganizationStaff

from fileroomio.models import FileItem

from newsdeskio.models import NewsdeskPost, NewsPostAccess

from mediaroomio.models import MediaImage


from ..serializers.news import (
    NewsListSerializer,
    NewsDetailSerializer,
    PrivateNewsPostFileListSerializer,
    PrivateNewsPostFileDetailSerializer,
    PrivatePostImageListSerializer,
    PrivatePostImageDetailSerializer,
)


class PrivateNewsList(generics.ListCreateAPIView):
    """View for creating and returning list of news of organization"""

    queryset = NewsdeskPost.objects.get_status_editable()
    serializer_class = NewsListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_fields = ["kind", "status"]
    ordering_fields = ["title", "created_at"]
    search_fields = [
        "author__first_name",
        "author__last_name",
        "organization__name",
        "summary",
        "title",
    ]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateNewsDetail(generics.RetrieveUpdateDestroyAPIView):
    """Detail view for organization news"""

    queryset = NewsdeskPost.objects.get_status_editable()
    serializer_class = NewsDetailSerializer
    permission_classes = [IsOrganizationStaff]
    lookup_field = "uid"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        news_uid = kwargs.get("uid", None)

        related = self.get_related_news(instance, news_uid)

        serializer = self.get_serializer(instance)
        data = {
            "object": serializer.data,
            "related": related,
        }
        return Response(data)

    def get_related_news(self, instance, news_uid):
        related_queryset = NewsdeskPost.objects.get_status_editable().exclude(
            uid=news_uid
        )
        related = related_queryset.order_by("?")[:3]
        serializer = self.get_serializer(related, many=True)
        return serializer.data

    def patch(self, request, *args, **kwargs):
        data = request.data
        if "access" in data:
            access = data["access"]
            newspost = self.get_object()
            newspost.newspostaccess_set.filter().delete()
            instances = []
            for item in access:
                uid = item["value"]
                newspostaccess = NewsPostAccess()
                try:
                    newspostaccess.newspost = newspost
                    newspostaccess.partner = Organization.objects.get(uid=uid)
                    instances.append(newspostaccess)
                except Organization.DoesNotExist:
                    continue
            newspostaccess = NewsPostAccess()
            newspostaccess.newspost = newspost
            newspostaccess.partner = newspost.organization
            instances.append(newspostaccess)
            NewsPostAccess.objects.bulk_create(instances)
        return super().patch(request, *args, **kwargs)


class PrivateNewsPostFileList(generics.ListCreateAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateNewsPostFileListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        news_post = get_object_or_404(NewsdeskPost, **kwargs)
        fileitem_ids = news_post.fileitemconnector_set.filter().values_list(
            "fileitem_id", flat=True
        )
        return self.queryset.filter(id__in=fileitem_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateNewsPostFileDetail(generics.RetrieveDestroyAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = PrivateNewsPostFileDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("newspost_uid", None)}
        return get_object_or_404(FileItem, **kwargs)


class PrivatePostImageList(generics.ListCreateAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PrivatePostImageListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        news_image = get_object_or_404(NewsdeskPost.objects.filter(), uid=uid)
        image_ids = news_image.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        return self.queryset.filter(id__in=image_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivatePostImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = PrivatePostImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("newsimage_uid", None)}
        return get_object_or_404(MediaImage, **kwargs)
