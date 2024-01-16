from django.db import models

from .choices import ModelKind


class NotificationManager(models.QuerySet):
    def create_new_product(self, organization, product, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            product=product,
            kind=kind,
            model_kind=ModelKind.PRODUCT,
            message=message,
        )
        return notification

    def create_new_project(self, organization, project, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            project=project,
            kind=kind,
            model_kind=ModelKind.PROJECT,
            message=message,
        )
        return notification
    
    def create_new_brand(self, organization, brand, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            brand=brand,
            kind=kind,
            model_kind=ModelKind.BRAND,
            message=message,
        )
        return notification

    def create_new_post(self, organization, post, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            post=post,
            kind=kind,
            model_kind=ModelKind.NEWS_DESK_POST,
            message=message,
        )
        return notification

    def create_organization_invite(
        self, organization, organization_invite, target, message, kind
    ):
        notification = self.create(
            organization=organization,
            target=target,
            organization_invite=organization_invite,
            kind=kind,
            model_kind=ModelKind.ORGANIZATION_INVITE,
            message=message,
        )
        return notification

    def create_group_invite(self, organization, member, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            member=member,
            kind=kind,
            model_kind=ModelKind.MEMBER,
            message=message,
        )
        return notification

    def create_new_product_discount(
        self, organization, discount, target, message, kind
    ):
        notification = self.create(
            organization=organization,
            target=target,
            discount=discount,
            kind=kind,
            model_kind=ModelKind.PRODUCT_DISCOUNT,
            message=message,
        )
        return notification

    def create_file_item_access(self, organization, file, target, message, kind):
        notification = self.create(
            organization=organization,
            target=target,
            file=file,
            kind=kind,
            model_kind=ModelKind.FILE_ITEM_ACCESS,
            message=message,
        )
        return notification
