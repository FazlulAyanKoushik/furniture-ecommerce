import stripe

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from paymentio.choices import (
    SubscriptionSessionStatus,
    SubscriptionTransactionStatus,
)
from paymentio.models import (
    SubscriptionSession,
    SubscriptionTransaction,
)


class Command(BaseCommand):
    help = "Automate monthly transactions for Pro organizations"

    def handle(self, *args, **options):
        stripe.api_key = settings.STRIPE_SECRET_KEY

        sessions = SubscriptionSession.objects.filter(
            status=SubscriptionSessionStatus.ACTIVE,
            plan__name="Pro",
        )

        for session in sessions:
            if session.next_payment_date <= timezone.now():
                self.process_payment(session)

    def process_payment(self, session):
        plan = session.plan
        amount = int(plan.price * 100)  # convert to cents
        currency = plan.currency

        try:
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=["card"],
            )

            SubscriptionTransaction.objects.create(
                session=session,
                status=SubscriptionTransactionStatus.SUCCESS,
                response_payload=payment_intent,
            )

            session.next_payment_date += timezone.timedelta(days=30)
            session.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Processed payment for organization {session.organization.name}"
                )
            )

        except stripe.error.StripeError as e:
            self.stdout.write(
                self.style.ERROR(
                    f"Error processing payment for session {session.id}: {str(e)}"
                )
            )
