from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404

from accountio.models import Organization

from core.rest.serializers import UserSlimSerializer

from threadio.choices import InboxKind, ThreadKind
from threadio.models import Inbox, Thread


class PrivateOrganizationThreadReplySerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = ["uid", "content", "author", "created_at"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        parent_uid = self.context["request"].parser_context["kwargs"].get("uid")

        parent = get_object_or_404(Thread.objects.filter(), uid=parent_uid)

        thread = Thread.objects.create(
            parent=parent,
            author=request_user,
            kind=ThreadKind.CHILD,
            **validated_data,
        )

        return thread


class PrivateOrganizationThreadSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)
    target = serializers.SlugRelatedField(
        slug_field="slug", queryset=Organization.objects.filter(), write_only=True
    )
    last_message = serializers.SerializerMethodField(read_only=True)

    def get_last_message(self, object_):
        last_message = (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(Q(parent=object_) | Q(pk=object_.pk))
            .order_by("-created_at")
            .first()
        )
        return PrivateOrganizationThreadReplySerializer(last_message).data

    class Meta:
        model = Thread
        fields = ["uid", "title", "content", "author", "target", "last_message"]

    def create(self, validated_data):
        target = validated_data.pop("target", None)
        request_user = self.context["request"].user
        organization = request_user.get_organization()

        if not target in organization.get_descendants():
            raise APIException(detail="You can't open a conversation")

        threads = Thread.objects.filter(
            inbox__organization=request_user.get_organization(), kind=ThreadKind.PARENT
        )

        inbox = Inbox.objects.filter(
            thread__in=list(threads), organization=target
        ).first()

        if inbox:
            thread = Thread.objects.create(
                parent=inbox.thread,
                author=request_user,
                kind=ThreadKind.CHILD,
                **validated_data,
            )

        else:
            thread = Thread.objects.create(
                author=request_user,
                kind=ThreadKind.PARENT,
                **validated_data,
            )
            Inbox.objects.bulk_create(
                [
                    Inbox(thread=thread, organization=instance, kind=InboxKind.SHARED)
                    for instance in [organization, target]
                ]
            )

        return thread
