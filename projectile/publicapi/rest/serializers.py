from rest_framework import serializers, throttling


# Serializer for the payload
class EmailContactFormSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=1, max_length=50)
    last_name = serializers.CharField(min_length=1, max_length=50)
    email = serializers.EmailField()
    phone = serializers.CharField(min_length=7, max_length=20)
    company = serializers.CharField(min_length=2, max_length=50)
    message = serializers.CharField(
        min_length=2,
        max_length=5000,
        help_text="Message must be less than or equal to 5000 characters.",
    )
