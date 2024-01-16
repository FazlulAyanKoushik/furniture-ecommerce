from rest_framework import serializers

from contentio.models import CustomerService


class PrivateCustomerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerService
        fields = ["uid", "slug", "name", "description", "status"]
        read_only_fields = ["uid", "slug"]
