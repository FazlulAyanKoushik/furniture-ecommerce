import os

from django.contrib.auth import get_user_model as User
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.rest.serializers.organization_users import (
    PublicOrganizationSlimSerializer,
    UserPrivateSerializer,
)

from collabio.models import (
    Project,
    ProjectParticipant,
)

from common.serializers import BaseModelSerializer
from common.fields import FileSizeField
from common.lists import FILE_EXTENSIONS

from mediaroomio.choices import MediaImageConnectorKind
from mediaroomio.models import (
    MediaImage,
    MediaImageConnector,
    MediaImageKind,
)

from fileroomio.choices import FileItemConnectorKind
from fileroomio.models import (
    FileItem,
    FileItemConnector,
)


class PrivateProjectListSerializer(BaseModelSerializer):
    """Serializer class for Project"""

    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
        ],
        required=False,
    )
    summary = serializers.CharField(max_length=1000, required=False)
    description = serializers.CharField(max_length=10000, required=False)
    location = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    date_start = serializers.DateField(required=False)
    date_stop = serializers.DateField(required=False)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "uid",
            "title",
            "slug",
            "organization",
            "summary",
            "description",
            "location",
            "country",
            "image",
            "date_start",
            "date_stop",
            "status",
            "visibility",
            "created_at",
        ]
        read_only_fields = ["uid", "slug"]

    def create(self, validated_data):
        organization = self.context["request"].user.get_organization()
        project = Project.objects.create(organization=organization, **validated_data)

        # Create an image instance if the user placed an image when creating the project
        try:
            if project.image:
                image_object, _ = MediaImage.objects.get_or_create(
                    image=project.image,
                    defaults={
                        "organization": self.context["request"].user.get_organization(),
                        "kind": MediaImageKind.IMAGE,
                    },
                )
                MediaImageConnector.objects.create(
                    image=image_object,
                    kind=MediaImageConnectorKind.PROJECT,
                    project=project,
                    organization=self.context["request"].user.get_organization(),
                )
        except:
            pass

        return project


class PrivateProjectDetailSerializer(BaseModelSerializer):
    """Serializer class for Project"""

    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
        ],
        required=False,
    )
    summary = serializers.CharField(max_length=1000, required=False)
    description = serializers.CharField(max_length=10000, required=False)
    location = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    date_start = serializers.DateField(required=False)
    date_stop = serializers.DateField(required=False)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "title",
            "organization",
            "summary",
            "description",
            "location",
            "country",
            "image",
            "date_start",
            "date_stop",
            "status",
            "visibility",
        ]

    def update(self, instance, validated_data):
        image = validated_data.pop("image", None)

        # Create an image instance if the user placed an image when updating the project
        try:
            if image is not None:
                instance.image = image
                instance.save()
                image_object, _ = MediaImage.objects.get_or_create(
                    image=instance.image,
                    defaults={
                        "organization": self.context["request"].user.get_organization(),
                        "kind": MediaImageKind.IMAGE,
                    },
                )
                MediaImageConnector.objects.create(
                    image=image_object,
                    kind=MediaImageConnectorKind.PROJECT,
                    project=instance,
                    organization=self.context["request"].user.get_organization(),
                )
        except:
            pass

        return super().update(instance, validated_data)


class PrivateProjectParticipantListSerializer(BaseModelSerializer):
    """Serializer class for Project"""

    user_uid = serializers.UUIDField(required=False)
    user = UserPrivateSerializer(read_only=True)

    class Meta:
        model = ProjectParticipant
        fields = ["uid", "user", "role", "status", "user_uid"]

        read_only_fields = ["uid"]
        write_only = ["user_uid"]

    def create(self, validated_data):
        project_kwargs = {"uid": str(self.context["project_uid"])}
        user_uid = validated_data.pop("user_uid")
        return ProjectParticipant.objects.create(
            project=get_object_or_404(Project, **project_kwargs),
            user=get_object_or_404(User(), **{"uid": str(user_uid)}),
            **validated_data
        )


class PrivateProjectParticipantDetailSerializer(BaseModelSerializer):
    """Serializer class for Project"""

    user_uid = serializers.UUIDField(required=False)
    user = UserPrivateSerializer(read_only=True)

    class Meta:
        model = ProjectParticipant
        fields = ["user", "role", "status", "user_uid"]


class PrivateProjectFileListSerializer(BaseModelSerializer):
    size = FileSizeField(read_only=True)

    class Meta:
        model = FileItem
        fields = [
            "uid",
            "fileitem",
            "name",
            "size",
            "dotextension",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uid",
            "size",
            "dotextension",
            "extension",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        file = validated_data.get("fileitem", None)
        filename = validated_data.get("name", None)

        if file:
            name, dotextension = os.path.splitext(file.name)
            dotextension = dotextension.lower()
            if filename:
                name = filename
                file.name = name + dotextension

        validated_data.update(
            {
                "size": file.size,
                "name": name,
                "dotextension": dotextension[1:],
                "extension": FILE_EXTENSIONS.get(dotextension, "Others"),
            }
        )

        file_item = FileItem.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )
        project_uid = {"uid": self.context["uid"]}

        FileItemConnector.objects.create(
            fileitem=file_item,
            project=get_object_or_404(Project, **project_uid),
            kind=FileItemConnectorKind.PROJECT,
            organization=self.context["request"].user.get_organization(),
        )
        return file_item


class PrivateProjectFileDetailSerializer(BaseModelSerializer):
    size = FileSizeField(read_only=True)

    class Meta:
        model = FileItem
        fields = [
            "fileitem",
            "name",
            "size",
            "dotextension",
            "description",
            "kind",
            "extension",
            "visibility",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "size",
            "dotextension",
            "extension",
            "created_at",
            "updated_at",
        ]


class PrivateProjectImageListSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "uid",
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ["width", "height"]

    def create(self, validated_data):
        image_object = MediaImage.objects.create(
            organization=self.context["request"].user.get_organization(),
            kind=MediaImageKind.IMAGE,
            **validated_data
        )

        project_uid = {"uid": self.context["uid"]}
        MediaImageConnector.objects.create(
            image=image_object,
            project=get_object_or_404(Project, **project_uid),
            kind=MediaImageConnectorKind.PROJECT,
            organization=self.context["request"].user.get_organization(),
        )
        return image_object


class PrivateProjectImageDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ["width", "height"]


class PrivateProjectCoverImageDetailSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )

    class Meta:
        model = MediaImage
        fields = [
            "image",
            "width",
            "height",
            "caption",
            "copyright",
            "priority",
        ]
        read_only_fields = ["__all__"]
