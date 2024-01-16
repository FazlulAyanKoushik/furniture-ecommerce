from rest_framework import serializers

from ..models import ScrapProductData


class ScrapProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapProductData
        fields = [
            "organization",
            "category",
            "title",
            "description",
            "product_link",
            "image_link",
        ]
        read_only_fields = ["__all__"]
