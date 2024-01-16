from django.db.models import Q

from rest_framework import serializers

from accountio.models import Organization
from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer

from catalogio.choices import ServiceKind
from catalogio.models import Product

from invitio.choices import OrganizationInviteResponse
from invitio.models import OrganizationInvite

from weapi.rest.serializers.brands import PrivateBrandSlimSerializer

from versatileimagefield.serializers import VersatileImageFieldSerializer


class PrivateSalesDashboardSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    company_registration = serializers.CharField(read_only=True, source="status")
    total_service = serializers.SerializerMethodField(read_only=True)
    total_invite_sent = serializers.SerializerMethodField(read_only=True)
    total_invite_received = serializers.SerializerMethodField(read_only=True)
    total_partner = serializers.SerializerMethodField(read_only=True)
    total_product = serializers.SerializerMethodField(read_only=True)
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "slug",
            "name",
            "avatar",
            "hero",
            "logo_wide",
            "image",
            "summary",
            "company_registration",
            "country",
            "kind",
            "total_product",
            "total_service",
            "total_invite_sent",
            "total_invite_received",
            "total_partner",
        ]
        read_only_fields = ("__all__",)

    def get_name(self, instance):
        return instance.display_name or instance.name
    
    def get_total_product(self, instance):
        return instance.product_set.filter().get_status_editable().count()
    
    def get_total_service(self, instance):
        return instance.organizationserviceconnector_set.filter(
            Q(service__kind=ServiceKind.PRESET_SERVICE)
            | Q(service__kind=ServiceKind.SERVICE)
        ).count()

    def get_total_invite_sent(self, instance):
        return OrganizationInvite.objects.filter(
            organization=instance, response=OrganizationInviteResponse.PENDING
        ).count()

    def get_total_invite_received(self, instance):
        return OrganizationInvite.objects.filter(
            target=instance, response=OrganizationInviteResponse.PENDING
        ).count()

    def get_total_partner(self, instance):
        return instance.get_descendants().count()


class PrivateProductSalesDashboardSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at400", "crop__400x400"),
        ],
        required=False,
    )
    title = serializers.SerializerMethodField(read_only=True)
    brand = PrivateBrandSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "slug",
            "title",
            "image",
            "brand",
            "category",
            "status",
            "organization",
        ]

    def get_title(self, instance):
        return instance.display_title or instance.title
