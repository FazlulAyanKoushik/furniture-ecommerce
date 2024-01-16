from django.contrib import admin

from .models import (
    AdFeature,
    SingleSession,
    SingleTransaction,
    SubscriptionPlan,
    SubscriptionPlanFeature,
    SubscriptionPlanFeatureConnector,
    SubscriptionSession,
    SubscriptionTransaction,
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    model = SubscriptionPlan
    list_display = ["name", "slug", "price", "created_at"]
    search_fields = ["name", "created_at"]


@admin.register(SubscriptionPlanFeature)
class SubscriptionPlanFeatureAdmin(admin.ModelAdmin):
    model = SubscriptionPlanFeature
    list_display = ["name"]


admin.site.register(SubscriptionPlanFeatureConnector)


@admin.register(SubscriptionSession)
class SubscriptionSessionAdmin(admin.ModelAdmin):
    model = SubscriptionSession
    list_display = ["plan", "start_date", "stop_date"]


@admin.register(SubscriptionTransaction)
class SubscriptionTransactionAdmin(admin.ModelAdmin):
    model = SubscriptionTransaction
    list_display = ["created_at"]


@admin.register(AdFeature)
class AdFeatureAdmin(admin.ModelAdmin):
    list_display = ["slug", "price", "currency", "kind"]


admin.site.register(SingleSession)
admin.site.register(SingleTransaction)
