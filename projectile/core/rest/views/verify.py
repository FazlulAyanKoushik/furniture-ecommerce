from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status

from otpio.models import UserPhone, UserPhoneOTP
from otpio.choices import UserPhoneStatus, UserPhoneOTPStatus

from core.models import UserEmail
from core.rest.serializers import MeUserEmailSerializer


class UserEmailTokenConsume(APIView):
    queryset = UserEmail.objects.get_status_pending()
    serializer = MeUserEmailSerializer
    permission_classes = (AllowAny,)
    lookup_field = "token"

    def patch(self, request, token):
        instance = self.get_object()
        instance.consume_token()
        self.queryset.filter(email=instance.email).exclude(pk=instance.pk).delete()
        return Response(True)


class UserPhoneVerifyOtp(APIView):
    def post(self, request):
        try:
            otp = request.data.get("otp")
            get_otp = get_object_or_404(UserPhoneOTP.objects.filter(), otp=otp)

            if get_otp.is_expired():
                return Response(status.HTTP_400_BAD_REQUEST)
            else:
                get_otp.phone.is_status_active()
                get_otp.phone.save()
                get_otp.status = UserPhoneOTPStatus.CONSUMED
                get_otp.save()

                return True

        except get_otp.DoesNotExist:
            return False
