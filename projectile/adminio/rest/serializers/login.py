from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import get_object_or_404

from adminio.utils import get_tokens_for_user

User = get_user_model()


class PrivateSalesLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = get_object_or_404(User.objects.filter(), email=email)

        if not user.check_password(password):
            raise AuthenticationFailed(detail="Invalid credentials.")

        if not user.is_staff:
            raise AuthenticationFailed(
                detail="You are not allowed to log in on this page."
            )

        # Get JWT tokens
        tokens = get_tokens_for_user(user)
        validated_data["refresh"] = tokens["refresh"]
        validated_data["access"] = tokens["access"]

        return validated_data
