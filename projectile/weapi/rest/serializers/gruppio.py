from gruppio.models import Group, Member
from common.serializers import BaseModelSerializer


class GroupSeriailizer(BaseModelSerializer):
    class Meta:
        model = Group
        fields = [
            "uid",
            "name",
            "description",
            "avatar",
            "hero",
            "slug",
            "kind",
            "status",
            "country",
            "faq",
            "organization",
            "post_count",
            "member_count",
        ]

        read_only_fields = ["uid", "slug", "post_count", "member_count"]


# member
class MemberSerializers(BaseModelSerializer):
    class Meta:
        model = Member
        fields = ["uid", "group", "user", "role", "status", "referrer", "token"]
        read_only_fields = ["uid", "token"]
