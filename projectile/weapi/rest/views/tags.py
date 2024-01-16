from rest_framework import filters, generics

from django_filters.rest_framework import DjangoFilterBackend

from tagio.choices import TagStatus
from tagio.models import Tag

from ..permissions import IsOrganizationDefaultStaff
from ..serializers import tags


class PrivateTagList(generics.ListCreateAPIView):
    queryset = Tag.objects.filter()
    serializer_class = tags.PrivateTagSerializer
    permission_classes = [IsOrganizationDefaultStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["name", "category"]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        tag_ids = organization.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        return self.queryset.filter(id__in=tag_ids)


class PrivateTagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.filter()
    serializer_class = tags.PrivateTagSerializer
    permission_classes = [IsOrganizationDefaultStaff]
    lookup_field = "uid"

    def perform_destroy(self, instance):
        instance.status = TagStatus.REMOVED
        instance.save()
