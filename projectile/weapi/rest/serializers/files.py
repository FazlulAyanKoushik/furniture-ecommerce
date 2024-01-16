import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from catalogio.models import Product

from gruppio.models import Group

from common.serializers import BaseModelSerializer

from collabio.models import Project

from fileroomio.choices import FileItemConnectorKind
from fileroomio.models import FileItem, FileItemConnector

from newsdeskio.models import NewsdeskPost

logger = logging.getLogger(__name__)



class FileSourceSerializer(BaseModelSerializer):
    """
    Serializer class to help files with information on where they belong
    le the file belong to a product it will provide-> type: PRODUCT and uid of the product
    """

    item_kind = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["item_kind", "uid"]
        read_only = "__all__"

    def __init__(self, *args, **kwargs):
        self.item_kind = kwargs.pop("item_kind", None)
        super().__init__(*args, **kwargs)

    def get_item_kind(self, obj):
        return self.item_kind
    

class PrivateOrganizationFileListSerializer(BaseModelSerializer):
    audience = serializers.SerializerMethodField()
    source = serializers.SerializerMethodField("get_source", read_only=True)

    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "source",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "organization_slug",
            "audience",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "uid",
            "source",
            "size",
            "dotextension",
            "organization_slug",
            "audience",
            "created_at",
            "updated_at",
        ]

    def get_audience(self, instance):
        audience = instance.fileitemaccess_set.exclude(
            partner=instance.organization
        ).select_related("partner")
        return [
            {
                "label": item.partner.display_name or item.partner.name,
                "value": item.partner.uid,
            }
            for item in audience
        ]

    def get_source(self, instance):
        """
        Gets the instance source's uid with source type
        Used multiple if elif condition as it needs Model object per kind
        TODO: Think of better solution to avoid multiple conditional statements
        """
        try:
            source = FileItemConnector.objects.get(fileitem=instance)

            if source.kind == FileItemConnectorKind.PRODUCT:
                product = Product.objects.get(id=source.product.id)
                return FileSourceSerializer(instance=product, item_kind=source.kind).data

            elif source.kind == FileItemConnectorKind.PROJECT:
                project = Project.objects.get(id=source.project.id)
                return FileSourceSerializer(instance=project, item_kind=source.kind).data

            elif source.kind == FileItemConnectorKind.GROUP:
                group = Group.objects.get(id=source.group.id)
                return FileSourceSerializer(instance=group, item_kind=source.kind).data

            elif source.kind == FileItemConnectorKind.NEWS_POST:
                news = NewsdeskPost.objects.get(id=source.newspost.id)
                return FileSourceSerializer(instance=news, item_kind=source.kind).data
            
        except Exception as _:
            return {}
        

    def create(self, validated_data, *args, **kwargs):
        description = validated_data["description"]
        kind = validated_data["kind"]
        visibility = validated_data["visibility"]
        status = validated_data["status"]
        fileitem = validated_data["fileitem"]

        name = validated_data["name"] or fileitem.name
        size = fileitem.size

        request = self.context["request"]
        user = request.user
        organization = user.get_organization()

        return FileItem.objects.create(
            name=name,
            description=description,
            size=size,
            kind=kind,
            visibility=visibility,
            status=status,
            fileitem=fileitem,
            user=user,
            organization=organization,
        )


class PrivateOrganizationFileDetailSerializer(BaseModelSerializer):
    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "size",
            "dotextension",
            "name",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "organization_slug",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "size",
            "extension",
            "dotextension",
            "organization_slug",
            "created_at",
            "updated_at",
        ]
