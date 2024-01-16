import logging

from django.conf import settings
from django.db import IntegrityError
from django.db.models import Max, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accountio.models import OrganizationUser
from accountio.rest.permissions import IsSameUser

from common.utils import get_client_ip

from notificationio.models import Notification

from otpio.generate_otp import otp_generator
from otpio.models import UserPhone, UserPhoneOTP


from threadio.choices import ThreadKind
from threadio.models import Inbox, Thread
from twilio.rest import Client

from ...emails import send_associated_email_verification_mail
from ..permissions import IsEmailOwner
from ..serializers import (
    MeOrganizationUserSerializer,
    MePasswordSerializer,
    MeSerializer,
    MeUserEmailSerializer,
    NotificationSerializer,
    PrivateThreadReplySerializer,
    PrivateThreadSerializer,
    PrivateUserPhoneSerializer,
)

logger = logging.getLogger(__name__)


class PrivateMeDetail(RetrieveUpdateAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


class PrivateMePassword(UpdateAPIView):
    serializer_class = MePasswordSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request):
        serializer = MePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(True, status=status.HTTP_200_OK)


class PrivateMeStatus(UpdateAPIView):
    serializer_class = MePasswordSerializer

    def get_object(self):
        return self.request.user

    def patch(self, request):
        data = request.data
        status_ = data["status"]
        if status_ in ["PAUSE", "UNPAUSE", "DELETE"]:
            instance = self.get_object()
            if status_ == "PAUSE" and instance.status != "PAUSED":
                instance.set_status_paused()
            elif status_ == "UNPAUSE" and instance.status != "ACTIVE":
                instance.set_status_unpaused()
            elif status_ == "DELETE" and instance.status != "REMOVED":
                instance.set_status_removed()
            return Response(True, status=status.HTTP_200_OK)
        return Response("Invalid request!", status=status.HTTP_400_BAD_REQUEST)


class PrivateMeUserEmailList(generics.ListCreateAPIView):
    serializer_class = MeUserEmailSerializer

    def get_queryset(self):
        queryset = self.request.user.useremail_set.filter()
        return queryset

    def post(self, request, format=None):
        serializer = MeUserEmailSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                instance = serializer.save(
                    user=request.user, ip_address=get_client_ip(request)
                )
                send_associated_email_verification_mail(instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {"email": ["Email already exists!"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrivateMeUserEmailDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MeUserEmailSerializer
    permissions = (IsEmailOwner,)
    lookup_field = "uid"

    def get_queryset(self):
        queryset = self.request.user.useremail_set.filter()
        return queryset


class PrivateMeOrganizationUserList(ListAPIView):
    """Provides logged-in user Organizations"""

    queryset = OrganizationUser.objects.none()
    serializer_class = MeOrganizationUserSerializer
    permission_classes = [IsSameUser]

    def get_queryset(self):
        # getting profiles under Organization User
        queryset = self.request.user.get_profiles()
        return queryset


class PrivateMeOrganizationUserSelect(APIView):
    def get_queryset(self):
        queryset = self.request.user.get_profiles()
        return queryset

    def patch(self, request, uid, format=None):
        profile = self.get_queryset().get(uid=uid)
        profile.select()
        serializer = MeOrganizationUserSerializer(profile)
        return Response(serializer.data)


class PrivateUserPhoneList(generics.ListCreateAPIView):
    queryset = UserPhone.objects.get_status_editable()
    serializer_class = PrivateUserPhoneSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.userphone_set.filter()
        return queryset


class PrivateUserPhoneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPhone.objects.get_status_editable()
    serializer_class = PrivateUserPhoneSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        return get_object_or_404(UserPhone, **kwargs)


class PrivateUserPhoneResendOtp(APIView):
    def post(self, request):
        phone_uid = request.get("uid")

        today = timezone.now().date()

        kwargs = {"uid": phone_uid, "user": request.user}

        user_phone = get_object_or_404(UserPhone.objects.filter(), **kwargs)

        get_otps = UserPhoneOTP.objects.filter(
            created_at__date=today, phone=user_phone
        ).count()

        if get_otps <= 2:
            otp = otp_generator()
            UserPhoneOTP.objects.create(phone=user_phone, otp=otp)

            # send OTP via SMS using Twilio
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f"Your OTP is: {otp}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=user_phone.phone,
            )

            return Response(
                {"status": status.HTTP_200_OK, "OTP": otp, "message": "OTP sent."}
            )

        return Response(status.HTTP_400_BAD_REQUEST)


class PrivateNotificationList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            target=request.user.get_organization()
        )

        response_data = {
            "count": notifications.count(),
            "unread_count": notifications.filter(is_unread=True).count(),
            "results": NotificationSerializer(notifications, many=True).data,
        }
        return Response(response_data)


class PrivateNotificationDetail(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        notification = get_object_or_404(Notification.objects.filter(), uid=uid)
        notification.mark_as_read()
        notification.save()
        return notification


class PrivateThreadList(generics.ListCreateAPIView):
    serializer_class = PrivateThreadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(inbox__user=self.request.user, kind=ThreadKind.PARENT)
            .annotate(last_message_time=Max("replies__created_at"))
            .order_by("-last_message_time", "-created_at")
        )


class PrivateThreadReplyList(generics.ListCreateAPIView):
    serializer_class = PrivateThreadReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        parent = get_object_or_404(
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(),
            uid=uid,
        )

        try:
            inbox = Inbox.objects.filter(thread=parent, user=self.request.user).first()
            if inbox and inbox.unread_count > 0:
                inbox.mark_as_read()

        except Inbox.DoesNotExist:
            pass

        return (
            Thread.objects.select_related("author")
            .prefetch_related("participants")
            .filter(Q(parent=parent) | Q(pk=parent.pk))
            .order_by("-created_at")
        )
