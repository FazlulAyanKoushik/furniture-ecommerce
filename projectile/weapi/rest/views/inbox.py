from django.db.models import Q, Max

from rest_framework import generics

from accountio.rest.permissions import IsOrganizationStaff

from threadio.choices import ThreadKind
from threadio.models import Thread

from ..serializers.inbox import (
    PrivateOrganizationThreadReplySerializer,
    PrivateOrganizationThreadSerializer,
)


class PrivateOrganizationThreadList(generics.ListCreateAPIView):
    serializer_class = PrivateOrganizationThreadSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        return (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(
                inbox__organization=self.request.user.get_organization(),
                kind=ThreadKind.PARENT,
            )
            .annotate(last_message_time=Max("replies__created_at"))
            .order_by("-last_message_time", "-created_at")
        )


class PrivateOrganizationThreadReplyList(generics.ListCreateAPIView):
    serializer_class = PrivateOrganizationThreadReplySerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        parent = generics.get_object_or_404(
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(),
            uid=uid,
        )
        return (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(Q(parent=parent) | Q(pk=parent.pk))
            .order_by("-created_at")
        )
