from django.db import models
from django.utils import timezone

from autoslug import AutoSlugField

from common.choices import Currency
from common.models import BaseModelWithUID

from .choices import (
    AdFeatureKind,
    SingleSessionStatus,
    SingleSessionKind,
    SingleTransactionStatus,
    SubscriptionPlanStatus,
    SubscriptionSessionStatus,
    SubscriptionTransactionStatus,
)
from .managers import SubscriptionPlanQuerySet, SubscriptionSessionQuerySet
from .utils import get_payment_slug, get_adfeature_slug


class SubscriptionPlan(BaseModelWithUID):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=600, blank=True)
    slug = AutoSlugField(populate_from=get_payment_slug, unique=True)
    price = models.DecimalField(max_digits=19, decimal_places=3, default=0)
    discounted_price = models.DecimalField(max_digits=19, decimal_places=3, default=0)
    currency = models.CharField(max_length=3, default="SEK")
    status = models.CharField(
        max_length=20,
        choices=SubscriptionPlanStatus.choices,
        default=SubscriptionPlanStatus.DRAFT,
    )
    objects = SubscriptionPlanQuerySet.as_manager()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class SubscriptionPlanFeature(BaseModelWithUID):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SubscriptionPlanFeatureConnector(BaseModelWithUID):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    feature = models.ForeignKey(SubscriptionPlanFeature, on_delete=models.CASCADE)

    def __str__(self):
        return f"Plan: {self.plan.name}, Feature: {self.feature.name}"


class SubscriptionSession(BaseModelWithUID):
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    stop_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=SubscriptionSessionStatus.choices,
        default=SubscriptionSessionStatus.ACTIVE,
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    client_secret = models.CharField(max_length=255, blank=True)
    payment_intent_id = models.CharField(max_length=255, blank=True)

    objects = SubscriptionSessionQuerySet.as_manager()

    class Meta:
        unique_together = ("organization", "plan")
        index_together = ("organization", "plan")
        ordering = ("-created_at",)

    def __str__(self):
        return f"Plan: {self.plan.name}, Organization: {self.organization.name}, Updated_at: {self.updated_at}"

    def stop(self):
        self.stop_date = timezone.now()
        self.save_dirty_fields()

    def is_active(self):
        return self.status == SubscriptionSessionStatus.ACTIVE

    def get_last_transaction(self):
        # Return the last transaction made related to this session
        return self.subscriptiontransaction_set.filter().latest()

    def cancel(self):
        self.stop()
        self.status = SubscriptionSessionStatus.CLOSED
        self.save_dirty_fields()

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now()
            self.next_payment_date = self.start_date + timezone.timedelta(days=30)
            self.next_payment_date.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )
        super().save(*args, **kwargs)


class SubscriptionTransaction(BaseModelWithUID):
    session = models.ForeignKey(
        SubscriptionSession, on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=30,
        choices=SubscriptionTransactionStatus.choices,
        default=SubscriptionTransactionStatus.PENDING,
    )
    response_payload = models.JSONField(default=dict)

    def __str__(self):
        return f"UID: {self.uid}"


class AdFeature(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_adfeature_slug, unique=True)
    message = models.CharField(max_length=600, blank=True)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.EUR
    )
    price = models.DecimalField(max_digits=19, decimal_places=3, default=0)
    kind = models.CharField(max_length=30, choices=AdFeatureKind.choices)

    def __str__(self) -> str:
        return f"KIND: {self.kind}, PRICE: {self.price}, CURRENCY: {self.currency}"


class SingleSession(BaseModelWithUID):
    status = models.CharField(
        max_length=20,
        choices=SingleSessionStatus.choices,
        default=SingleSessionStatus.PENDING,
    )
    payment_intent_id = models.CharField(max_length=100, blank=True)
    client_secret = models.CharField(max_length=255, blank=True)
    # Foreignkeys
    organization = models.ForeignKey(
        "adio.AdOrganization", on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        "adio.AdProduct", on_delete=models.SET_NULL, null=True, blank=True
    )
    project = models.ForeignKey(
        "adio.AdProject", on_delete=models.SET_NULL, null=True, blank=True
    )
    kind = models.CharField(max_length=30, choices=SingleSessionKind.choices)

    def __str__(self) -> str:
        try:
            if self.kind == SingleSessionKind.ORGANIZATION:
                return f"UID: {self.uid}, Organization: {self.organization.organization.name}"
            if self.kind == SingleSessionKind.PRODUCT:
                return f"UID: {self.uid}, Product: {self.product.product.title}"
            if self.kind == SingleSessionKind.PROJECT:
                return f"UID: {self.uid}, Project: {self.project.project.title}"

        except AttributeError:
            pass
        return None


class SingleTransaction(BaseModelWithUID):
    session = models.ForeignKey(SingleSession, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=30,
        choices=SingleTransactionStatus.choices,
        default=SingleTransactionStatus.PENDING,
    )
    response_payload = models.JSONField(default=dict)

    def __str__(self):
        return f"UID: {self.uid}"
