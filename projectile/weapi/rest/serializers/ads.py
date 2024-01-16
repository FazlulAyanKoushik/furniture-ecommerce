from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization
from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from adio.models import AdOrganization, AdProduct, AdProject

from catalogio.models import Product

from collabio.models import Project

from common.serializers import BaseModelSerializer

from paymentio.models import AdFeature

from .brands import PrivateBrandSlimSerializer
from ..serializers.products import PrivateMaterialSlimSerializer


class PrivateAdFeatureSerializer(BaseModelSerializer):
    class Meta:
        model = AdFeature
        fields = ["uid", "slug", "message", "currency", "price", "kind"]


class PrivateProductAdSlimSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )
    brand = PrivateBrandSlimSerializer(read_only=True)
    materials = PrivateMaterialSlimSerializer(
        read_only=True, many=True, source="productmaterialconnector_set"
    )

    class Meta:
        model = Product
        fields = [
            "slug",
            "title",
            "display_title",
            "image",
            "description",
            "categories",
            "color",
            "material",
            "status",
            "brand",
            "materials",
        ]
        read_only_fields = ["__all__"]


class PrivateProductAdSerializer(BaseModelSerializer):
    adfeature = PrivateAdFeatureSerializer(read_only=True)
    adfeature_uid = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=AdFeature.objects.filter(),
        write_only=True,
    )
    product = PrivateProductAdSlimSerializer(read_only=True)
    product_uid = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=Product.objects.get_status_active(),
        write_only=True,
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)
    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = AdProduct
        fields = [
            "uid",
            "slug",
            "product",
            "product_uid",
            "organization",
            "start_date",
            "ad_days",
            "stop_date",
            "view_count",
            "click_count",
            "adfeature",
            "adfeature_uid",
            "status",
            "client_secret",
            "total_price",
        ]
        read_only_fields = [
            "uid",
            "slug",
            "product",
            "organization",
            "stop_date",
            "status",
            "view_count",
            "click_count",
            "adfeature",
            "client_secret",
            "total_price",
        ]

    def create(self, validated_data):
        organization = self.context["request"].user.get_organization()
        product_uid = validated_data.pop("product_uid", None)
        adfeature_uid = validated_data.pop("adfeature_uid", None)
        validated_data["organization"] = organization
        ad_product = get_object_or_404(
            Product.objects.get_status_active(),
            uid=product_uid.uid,
            organization=organization,
        )

        return AdProduct.objects.create(
            product=ad_product, adfeature=adfeature_uid, **validated_data
        )

    def get_client_secret(self, object_):
        return object_.singlesession_set.filter().first().client_secret


class PrivateProjectAdSlimSerializer(BaseModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400x300", "thumbnail__400x300"),
        ],
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            "slug",
            "title",
            "summary",
            "description",
            "location",
            "country",
            "image",
            "visibility",
        ]
        read_only_fields = ["__all__"]


class PrivateProjectAdSerializer(BaseModelSerializer):
    adfeature = PrivateAdFeatureSerializer(read_only=True)
    adfeature_uid = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=AdFeature.objects.filter(),
        write_only=True,
    )
    client_secret = serializers.SerializerMethodField()
    organization = PublicOrganizationSlimSerializer(read_only=True)
    project = PrivateProjectAdSlimSerializer(read_only=True)
    project_uid = serializers.SlugRelatedField(
        queryset=Project.objects.get_status_active(),
        slug_field="uid",
        write_only=True,
    )

    class Meta:
        model = AdProject
        fields = [
            "uid",
            "slug",
            "project_uid",
            "project",
            "organization",
            "start_date",
            "ad_days",
            "stop_date",
            "view_count",
            "click_count",
            "adfeature",
            "adfeature_uid",
            "status",
            "client_secret",
            "total_price",
        ]
        read_only_fields = [
            "uid",
            "slug",
            "project",
            "organization",
            "stop_date",
            "status",
            "view_count",
            "click_count",
            "adfeature",
            "client_secret",
            "total_price",
        ]

    def create(self, validated_data):
        organization = self.context["request"].user.get_organization()
        project_uid = validated_data.pop("project_uid", None)
        adfeature_uid = validated_data.pop("adfeature_uid", None)
        validated_data["organization"] = organization
        ad_project = get_object_or_404(
            Project.objects.get_status_active(),
            uid=project_uid.uid,
            organization=organization,
        )

        return AdProject.objects.create(
            project=ad_project, adfeature=adfeature_uid, **validated_data
        )

    def get_client_secret(self, object_):
        return object_.singlesession_set.filter().first().client_secret


class PrivateOrganizationAdSerializer(serializers.ModelSerializer):
    adfeature = PrivateAdFeatureSerializer(read_only=True)
    adfeature_uid = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=AdFeature.objects.filter(),
        write_only=True,
    )
    client_secret = serializers.SerializerMethodField()
    organization = PublicOrganizationSlimSerializer(read_only=True)
    organization_uid = serializers.SlugRelatedField(
        slug_field="uid",
        queryset=Organization.objects.get_status_active(),
        write_only=True,
    )

    class Meta:
        model = AdOrganization
        fields = [
            "uid",
            "slug",
            "organization",
            "organization_uid",
            "start_date",
            "ad_days",
            "stop_date",
            "view_count",
            "click_count",
            "adfeature",
            "adfeature_uid",
            "status",
            "client_secret",
            "total_price",
        ]
        read_only_fields = [
            "uid",
            "slug",
            "organization",
            "stop_date",
            "view_count",
            "click_count",
            "adfeature",
            "status",
            "client_secret",
            "total_price",
        ]

    def create(self, validated_data):
        adfeature_uid = validated_data.pop("adfeature_uid", None)
        organization = validated_data.pop("organization_uid", None)
        ad_organization = get_object_or_404(
            Organization.objects.get_status_active(), uid=organization.uid
        )

        return AdOrganization.objects.create(
            organization=ad_organization, adfeature=adfeature_uid, **validated_data
        )

    def get_client_secret(self, object_):
        return object_.singlesession_set.filter().first().client_secret
