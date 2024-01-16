import stripe

from django.conf import settings
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accountio.models import Organization
from accountio.rest.permissions import IsOrganizationStaff

from paymentio.choices import SubscriptionSessionStatus
from paymentio.models import SubscriptionSession, SubscriptionTransaction
from paymentio.rest.serializers.subscription_plan import SubscriptionSessionSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


class PrivateSubscriptionSessionList(generics.ListCreateAPIView):
    queryset = SubscriptionSession.objects.get_status_active()
    serializer_class = SubscriptionSessionSerializer
    permission_classes = [IsOrganizationStaff]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data.get("status") == SubscriptionSessionStatus.ACTIVE:
            try:
                plan = serializer.validated_data.get("plan", None)
                existing_session = SubscriptionSession.objects.filter(
                    plan=plan, organization=self.request.user.get_organization()
                ).first()
                if existing_session:
                    return Response(
                        {"detail": "This plan has already been purchased."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                session = serializer.save()
                transaction = self.create_subscription_transaction(
                    serializer.validated_data, session
                )
                serializer.validated_data["client_secret"] = transaction.client_secret
                serializer.validated_data[
                    "payment_intent_id"
                ] = transaction.payment_intent_id
                serializer.save()
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            except stripe.error.StripeError as e:
                error_message = str(e)
                return Response(
                    {"error": error_message},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def create_subscription_transaction(self, validated_data, session):
        plan = validated_data["plan"]
        amount = int(plan.price * 100)  # convert to cents
        currency = plan.currency

        transaction = SubscriptionTransaction()
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Create a PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            description="Pro Membership",
        )

        transaction.client_secret = payment_intent.client_secret
        transaction.payment_intent_id = payment_intent.id
        transaction.session = session  # validated_data.get("session")
        transaction.response_payload = payment_intent
        transaction.save()
        return transaction

    def perform_create(self, serializer):
        serializer.validated_data["start_date"] = timezone.now()
        serializer.validated_data["stop_date"] = serializer.validated_data[
            "start_date"
        ] + timezone.timedelta(days=30)
        super().perform_create(serializer)

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return SubscriptionSession.objects.get_status_active().filter(
            organization=organization
        )


class PrivateOrganizationProSubscriptionDetail(APIView):
    def get(self, request, organization_slug):
        kwargs = {"slug": organization_slug}
        organization = generics.get_object_or_404(
            Organization.objects.filter(), **kwargs
        )

        if organization.has_pro_subscription():
            return Response({"True"}, status.HTTP_200_OK)
        else:
            return Response({"False"}, status.HTTP_200_OK)
