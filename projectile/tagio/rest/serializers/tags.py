from rest_framework import serializers

from ...models import Tag


class TagSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = (
            "name",
            "slug",
            "i18n",
            "options",
        )

    def get_options(self, object_):
        tags = object_.children.filter(status="ACTIVE")
        return TagSerializer(tags, many=True).data
