import logging

import stripe

from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from paymentio.choices import SingleSessionStatus, SingleTransactionStatus
from paymentio.models import SingleSession, SingleTransaction


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


@method_decorator(csrf_exempt, name="dispatch")
class AdTransactionStatusWebhook(APIView):
    permission_classes = []

    def post(self, request, format=None):
        payload = request.body.decode("utf-8")
        signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
        try:
            event = stripe.Webhook.construct_event(
                payload, signature_header, settings.STRIPE_WEBHOOK_SIGNING_SECRET
            )
        except ValueError as e:
            logger.error("A ValueError occurred: %s", str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)

        event_type = event.type

        if event_type == "payment_intent.succeeded" or event_type == "charge.succeeded":
            payment_intent = event.data.object
            transaction_id = payment_intent.id
            try:
                session = SingleSession.objects.get(payment_intent=transaction_id)
                session.status = SingleSessionStatus.ACTIVE
                session.save()
                transaction = SingleTransaction.objects.get(
                    session__payment_intent_id=transaction_id
                )
                transaction.status = SingleTransactionStatus.SUCCEEDED
                transaction.save()
            except SingleTransaction.DoesNotExist:
                pass

        elif event_type == "payment_intent.canceled":
            payment_intent = event.data.object
            transaction_id = payment_intent.id
            try:
                session = SingleSession.objects.get(payment_intent=transaction_id)
                session.status = SingleSessionStatus.PENDING
                session.save()
                transaction = SingleTransaction.objects.get(
                    session__payment_intent_id=transaction_id
                )
                transaction.status = SingleTransactionStatus.CANCELLED
                transaction.save()
            except SingleTransaction.DoesNotExist:
                pass

        elif event_type == "payment_intent.payment_failed":
            payment_intent = event.data.object
            transaction_id = payment_intent.id
            try:
                session = SingleSession.objects.get(payment_intent=transaction_id)
                session.status = SingleSessionStatus.PENDING
                session.save()
                transaction = SingleTransaction.objects.get(
                    session__payment_intent_id=transaction_id
                )
                transaction.status = SingleTransactionStatus.FAILED
                transaction.save()
            except SingleTransaction.DoesNotExist:
                pass

        return Response(status=status.HTTP_200_OK)
