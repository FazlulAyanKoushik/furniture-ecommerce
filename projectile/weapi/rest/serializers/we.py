import logging

from django.db import transaction

from rest_framework import serializers

from accountio.models import Organization

from common.serializers import BaseModelSerializer

from tagio.models import Tag, TagConnector

from versatileimagefield.serializers import VersatileImageFieldSerializer

from weapi.rest.serializers import tags

logger = logging.getLogger(__name__)


class PrivateWeOrganizationSerializer(BaseModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    registration_no = serializers.CharField(min_length=2)
    tags = serializers.SerializerMethodField("get_tags", required=False)
    tag_uids = serializers.ListField(write_only=True, required=False)
    subscription_plans = serializers.SerializerMethodField(read_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "uid",
            "name",            
            "email",
            "slug",
            "registration_no",
            "subscription_plans",
            "address",
            "postal_code",
            "postal_area",
            "city",
            "country",
            "summary",
            "avatar",
            "hero",
            "image",
            "logo_wide",
            "description",
            "status",
            "categories",
            "kind",
            "phone",
            "website_url",
            "tags",
            "tag_uids",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "created_at", "updated_at"]

    def get_name(self, instance):
        return instance.display_name or instance.name

    def get_tags(self, instance):
        """show the connected tag list"""
        tag_connectors = instance.tagconnector_set.filter().values_list(
            "tag_id", flat=True
        )
        tag_queryset = Tag.objects.filter(id__in=tag_connectors)
        return tags.PrivateTagSerializer(tag_queryset, many=True).data

    def get_subscription_plans(self, instance):
        subscription = instance.subscriptionsession_set.filter().values(
            "plan__name",
            "start_date",
            "next_payment_date",
            "stop_date",
            "status",
            "client_secret",
        )
        return subscription

    def update(self, instance, validated_data):
        tag_uids = validated_data.pop("tag_uids", [])
        existing_tag_ids = TagConnector.objects.filter(
            organization=instance
        ).values_list("tag__id", flat=True)

        tags = Tag.objects.filter(uid__in=tag_uids).exclude(id__in=existing_tag_ids)
        new_tag_connectors = [
            TagConnector(tag=tag, organization=instance) for tag in tags
        ]

        with transaction.atomic():
            TagConnector.objects.bulk_create(new_tag_connectors)
            return super().update(instance, validated_data)
