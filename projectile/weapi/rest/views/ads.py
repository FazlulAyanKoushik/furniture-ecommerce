import stripe

from django.conf import settings
from django.utils import timezone

from rest_framework import generics, status
from rest_framework.response import Response

from accountio.rest.permissions import IsOrganizationStaff

from adio.choices import DaysValidityStatus
from adio.models import AdOrganization, AdProduct, AdProject

from paymentio.choices import AdFeatureKind, SingleTransactionStatus
from paymentio.models import AdFeature, SingleSession, SingleTransaction
from paymentio.helpers import InvalidAdFeatureKind

from ..serializers.ads import (
    PrivateAdFeatureSerializer,
    PrivateOrganizationAdSerializer,
    PrivateProductAdSerializer,
    PrivateProjectAdSerializer,
)


stripe.api_key = settings.STRIPE_SECRET_KEY


class PrivateOrganizationAdFeatureList(generics.ListAPIView):
    queryset = AdFeature.objects.filter()
    serializer_class = PrivateAdFeatureSerializer
    permission_classes = [IsOrganizationStaff]


class PrivateOrganizationAdList(generics.ListCreateAPIView):
    serializer_class = PrivateOrganizationAdSerializer
    permission_classes = [IsOrganizationStaff]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adfeature = serializer.validated_data.get("adfeature_uid", None)

        if adfeature.kind != AdFeatureKind.ORGANIZATION:
            raise InvalidAdFeatureKind(
                "This is not a valid organization adfeature kind."
            )

        start_date = serializer.validated_data.get("start_date", None)
        ad_days = serializer.validated_data.get("ad_days", None)
        if ad_days == DaysValidityStatus.DAYS_30:
            stop_date = start_date + timezone.timedelta(days=29)
        elif ad_days == DaysValidityStatus.DAYS_60:
            stop_date = start_date + timezone.timedelta(days=59)
        total_price = ((stop_date - start_date).days + 1) * adfeature.price
        serializer.save(total_price=total_price, stop_date=stop_date)

        # Create a PaymentIntent
        amount = int(total_price * 100)
        currency = adfeature.currency
        organization = serializer.validated_data.get("organization_uid")
        start_date = serializer.validated_data.get("start_date")
        stop_date = stop_date

        metadata = {}
        if organization:
            promoted_organization = organization
            metadata["promoted_organization"] = promoted_organization.name
            metadata["organization"] = organization.name
            metadata["start_date"] = start_date
            metadata["stop_date"] = stop_date
            metadata["adfeature"] = adfeature

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            description=f"Promote {promoted_organization.name}!",
            metadata=metadata,
        )

        session_data = {
            "payment_intent_id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "organization": serializer.instance,
            "kind": adfeature.kind,
        }
        session = SingleSession.objects.create(**session_data)

        transaction_data = {
            "session": session,
            "status": SingleTransactionStatus.PENDING,
            "response_payload": payment_intent,
        }
        SingleTransaction.objects.create(**transaction_data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return AdOrganization.objects.get_status_fair().filter(
            organization=organization
        )


class PrivateOrganizationAdDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PrivateOrganizationAdSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        ad_organization = generics.get_object_or_404(
            AdOrganization.objects.get_status_fair(), uid=uid
        )
        ad_organization.increment_count()
        return ad_organization


class PrivateProductAdList(generics.ListCreateAPIView):
    serializer_class = PrivateProductAdSerializer
    permission_classes = [IsOrganizationStaff]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adfeature = serializer.validated_data.get("adfeature_uid", None)

        if adfeature.kind != AdFeatureKind.PRODUCT:
            raise InvalidAdFeatureKind("This is not a valid product adfeature kind.")

        start_date = serializer.validated_data.get("start_date", None)
        ad_days = serializer.validated_data.get("ad_days", None)
        if ad_days == DaysValidityStatus.DAYS_30:
            stop_date = start_date + timezone.timedelta(days=29)
        elif ad_days == DaysValidityStatus.DAYS_60:
            stop_date = start_date + timezone.timedelta(days=59)
        total_price = ((stop_date - start_date).days + 1) * adfeature.price
        serializer.save(total_price=total_price, stop_date=stop_date)

        # Create a PaymentIntent
        amount = int(total_price * 100)
        currency = adfeature.currency
        product = serializer.validated_data.get("product_uid")
        start_date = serializer.validated_data.get("start_date")
        stop_date = stop_date

        metadata = {}
        if product:
            promoted_product = product
            metadata["promoted_product"] = promoted_product.title
            metadata["organization"] = product.organization.name
            metadata["start_date"] = start_date
            metadata["stop_date"] = stop_date
            metadata["adfeature"] = adfeature

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            description=f"Promote {promoted_product.title}!",
            metadata=metadata,
        )

        session_data = {
            "payment_intent_id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "product": serializer.instance,
            "kind": adfeature.kind,
        }
        session = SingleSession.objects.create(**session_data)

        transaction_data = {
            "session": session,
            "status": SingleTransactionStatus.PENDING,
            "response_payload": payment_intent,
        }
        SingleTransaction.objects.create(**transaction_data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return AdProduct.objects.get_status_fair().filter(organization=organization)


class PrivateProductAdDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PrivateProductAdSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        ad_product = generics.get_object_or_404(
            AdProduct.objects.get_status_fair(), uid=uid
        )
        ad_product.increment_count()
        return ad_product


class PrivateProjectAdList(generics.ListCreateAPIView):
    serializer_class = PrivateProjectAdSerializer
    permission_classes = [IsOrganizationStaff]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        adfeature = serializer.validated_data.get("adfeature_uid", None)

        if adfeature.kind != AdFeatureKind.PROJECT:
            raise InvalidAdFeatureKind("This is not a valid project adfeature kind.")

        start_date = serializer.validated_data.get("start_date", None)
        ad_days = serializer.validated_data.get("ad_days", None)
        if ad_days == DaysValidityStatus.DAYS_30:
            stop_date = start_date + timezone.timedelta(days=29)
        elif ad_days == DaysValidityStatus.DAYS_60:
            stop_date = start_date + timezone.timedelta(days=59)
        total_price = ((stop_date - start_date).days + 1) * adfeature.price
        serializer.save(total_price=total_price, stop_date=stop_date)

        # Create a PaymentIntent
        amount = int(total_price * 100)
        currency = adfeature.currency
        project = serializer.validated_data.get("project_uid")
        start_date = serializer.validated_data.get("start_date")
        stop_date = serializer.validated_data.get("stop_date")

        metadata = {}
        if project:
            promoted_project = project
            metadata["promoted_project"] = promoted_project.title
            metadata["organization"] = project.organization.name
            metadata["start_date"] = start_date
            metadata["stop_date"] = stop_date
            metadata["adfeature"] = adfeature

        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
            description=f"Promote {promoted_project.title}!",
            metadata=metadata,
        )

        session_data = {
            "payment_intent_id": payment_intent.id,
            "client_secret": payment_intent.client_secret,
            "project": serializer.instance,
            "kind": adfeature.kind,
        }
        session = SingleSession.objects.create(**session_data)

        transaction_data = {
            "session": session,
            "status": SingleTransactionStatus.PENDING,
            "response_payload": payment_intent,
        }
        SingleTransaction.objects.create(**transaction_data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return AdProject.objects.get_status_fair().filter(organization=organization)


class PrivateProjectAdDetail(generics.RetrieveDestroyAPIView):
    serializer_class = PrivateProjectAdSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        uid = self.kwargs.get("uid", None)
        ad_project = generics.get_object_or_404(
            AdProject.objects.get_status_fair(), uid=uid
        )
        ad_project.increment_count()
        return ad_project
