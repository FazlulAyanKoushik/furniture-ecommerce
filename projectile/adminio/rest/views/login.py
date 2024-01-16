from rest_framework import generics, status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.login import PrivateSalesLoginSerializer


class PrivateSalesLogin(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PrivateSalesLoginSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=data.data)
