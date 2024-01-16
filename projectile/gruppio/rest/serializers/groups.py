from accountio.rest.serializers.organizations import PublicOrganizationSlimSerializer
from accountio.rest.serializers.organization_users import PrivateUserSlimSerializer

from common.serializers import BaseModelSerializer

from gruppio.models import Group, Member

from versatileimagefield.serializers import VersatileImageFieldSerializer


class GlobalGroupListSeriailizer(BaseModelSerializer):
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    class Meta:
        model = Group
        fields = [
            "name",
            "description",
            "avatar",
            "hero",
            "slug",
            "kind",
            "status",
            "country",
            "faq",
            "post_count",
            "member_count",
        ]
        read_only_fields = ["__all__"]
        
        
class GlobalGroupDetailSeriailizer(BaseModelSerializer):
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x256", "crop__1024x256"),
        ],
        required=False,
    )
    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        required=False,
    )
    organization = PublicOrganizationSlimSerializer()
    class Meta:
        model = Group
        fields = [
            "name",
            "description",
            "avatar",
            "hero",
            "slug",
            "kind",
            "country",
            "organization",
            "post_count",
            "member_count",
        ]
        read_only_fields = ["__all__"]


class GlobalGroupSlimSerializer(BaseModelSerializer):
    class Meta:
        model = Group
        fields = [
            "slug",
            "name",
        ]
        read_only_fields = ("__all__",)


class GlobalMemberListSerializer(BaseModelSerializer):
    group = GlobalGroupSlimSerializer()
    user = PrivateUserSlimSerializer()
    class Meta:
        model = Member
        fields = ["uid", "group", "user", "role", "status", "referrer", "token"]
        read_only_fields = ["__all__"]
        
        
class GlobalMemberDetailSerializer(BaseModelSerializer):
    group = GlobalGroupSlimSerializer()
    user = PrivateUserSlimSerializer()
    class Meta:
        model = Member
        fields = ["group", "user", "role", "status", "referrer", "token"]
        read_only_fields = ["__all__"]


class GlobalAdminListSerializer(BaseModelSerializer):
    group = GlobalGroupSlimSerializer(read_only=True)
    user = PrivateUserSlimSerializer(read_only=True)
    class Meta:
        model = Member
        fields = ["uid", "group", "user", "role", "status", "referrer", "token"]
        read_only_fields = ["__all__"]
