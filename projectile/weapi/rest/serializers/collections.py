
from rest_framework import serializers

from common.serializers import BaseModelSerializer

from catalogio.models import ProductCollection, ProductCollectionBridge, Product


class PrivateOrganizationCollectionListSerializer(BaseModelSerializer):
    class Meta:
        model = ProductCollection
        fields = [
            "uid",
            "slug",
            "title",
            "kind",
            "visibility",
            "product_count",
        ]
        read_only_fields = ["product_count"]

    def create(self, validated_data):
        return ProductCollection.objects.create(
            organization=self.context["request"].user.get_organization(),
            **validated_data
        )


class PrivateOrganizationCollectionDetailSerializer(BaseModelSerializer):
    class Meta:
        model = ProductCollection
        fields = [
            "slug",
            "title",
            "kind",
            "visibility",
            "product_count",
        ]
        read_only_fields = ["slug", "product_count"]


class PrivateCollectionProducts(serializers.ModelSerializer):
    product_uids = serializers.ListField(child=serializers.UUIDField())

    class Meta:
        model = ProductCollection
        fields = ["product_uids"]

    def create(self, validated_data):
        product_bridge = []
        collection = ProductCollection.objects.get(uid=self.context["collection_uid"])

        for product in Product.objects.filter(uid__in=self.data["product_uids"]):
            product_bridge.append(
                ProductCollectionBridge(collection=collection, product=product)
            )

        bridge = ProductCollectionBridge.objects.bulk_create(product_bridge)
        return bridge
