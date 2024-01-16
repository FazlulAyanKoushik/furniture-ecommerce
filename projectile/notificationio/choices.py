from django.db import models


class NotificationKind(models.TextChoices):
    EVENT_POST = "EVENT_POST", "Event Post"
    GROUP_INVITE_REQUEST = "GROUP_INVITE_REQUEST", "Group Invite Request"
    GROUP_INVITE_ACCEPTED = "GROUP_INVITE_ACCEPTED", "Group Invite Accepted"
    GROUP_INVITE_REJECTED = "GROUP_INVITE_REJECTED", "Group Invite Rejected"
    INVITE_REQUEST = "INVITE_REQUEST", "Invite Request"
    INVITE_ACCEPTED = "INVITE_ACCEPTED", "Invite Accepted"
    INVITE_REJECTED = "INVITE_REJECTED", "Invite Rejected"
    NEW_BRAND = "NEW_BRAND", "New Brand"
    NEW_PRODUCT = "NEW_PRODUCT", "New Product"
    NEW_PROJECT = "NEW_PROJECT", "New Project"
    NEWS_POST = "NEWS_POST", "News Post"
    NEW_SERVICE = "NEW_SERVICE", "New Service"
    POST_REPLY = "POST_REPLY", "Post Reply"
    POST_LIKE = "POST_LIKE", "Post Like"
    PRODUCT_PRICING = "PRODUCT_PRICING", "Product Pricing"
    FILE = "FILE", "File"


class ModelKind(models.TextChoices):
    BRAND = "BRAND", "Brand"
    PRODUCT = "PRODUCT", "Product"
    PROJECT = "PROJECT", "Project"
    ORGANIZATION_INVITE = "ORGANIZATION_INVITE", "Organization Invite"
    MEMBER = "MEMBER", "Member"
    NEWS_DESK_POST = "NEWS_DESK_POST", "News Desk Post"
    PRODUCT_DISCOUNT = "PRODUCT_DISCOUNT", "Product Discount"
    FILE_ITEM_ACCESS = "FILE_ITEM_ACCESS", "File Item Access"
    SERVICE = "SERVICE", "Service"

class NotificationSettingsKind(models.TextChoices):
    ORGANIZATION = "ORGANIZATION", "Organization"
    USER = "USER", "User"
