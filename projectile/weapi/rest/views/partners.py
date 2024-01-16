import io

import pandas as pd

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accountio.models import Descendant, Organization
from accountio.rest.permissions import IsOrganizationStaff
from accountio.rest.serializers.organization_users import (
    PrivateOrganizationPartnerUserListSerializer,
)

from catalogio.models import ProductDiscount

from core.models import User

from fileroomio.models import FileItem, FileItemAccess

from invitio.models import OrganizationInvite

from ..serializers.partners import (
    PrivateBulkCreatePartnersSerializers,
    PrivateOrganizationPartnerSerializer,
    PrivateOrganizationPartnerDiscountSerializer,
    PrivateOrganizationPartnerFileItemSerializer,
    PrivatePartnerDiscountListSerializer,
)


class PrivateOrganizationPartnersList(generics.ListCreateAPIView):
    queryset = Organization.objects.none()
    serializer_class = PrivateOrganizationPartnerSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ["country", "kind", "segment"]
    search_fields = ["name", "display_name", "kind", "country"]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        if organization:
            child_ids = organization.descendant_set.filter().values_list(
                "child_id", flat=True
            )
            partners = (
                Organization.objects.get_status_fair()
                .filter(id__in=child_ids)
                .order_by("-organizationinvite__updated_at", "-invites__updated_at")
            )
            return partners
        # errors handle, if no organization found with is_default = True
        return self.queryset


class PrivateOrganizationPartnersDetail(generics.RetrieveDestroyAPIView):
    queryset = Organization.objects.get_status_fair()
    serializer_class = PrivateOrganizationPartnerSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        parent = self.request.user.get_organization()
        child = get_object_or_404(Organization, uid=self.kwargs.get("uid"))
        descendant = get_object_or_404(Descendant, parent=parent, child=child)
        organization = descendant.child
        return organization

    def destroy(self, request, *args, **kwargs):
        child = self.get_object()
        parent = self.request.user.get_organization()
        descendants = Descendant.objects.filter(
            Q(parent=parent, child=child) | Q(parent=child, child=parent)
        )
        descendants.delete()
        invites = OrganizationInvite.objects.filter(
            Q(organization=parent, target=child) | Q(organization=child, target=parent)
        ).filter(response__in=["ACCEPTED", "DECLINED"])
        invites.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PrivateOrganizationPartnersDiscountList(generics.ListAPIView):
    queryset = ProductDiscount.objects.filter()
    serializer_class = PrivatePartnerDiscountListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {
            "uid": self.kwargs.get("uid", None),
        }
        target = get_object_or_404(Organization.objects.get_status_fair(), **kwargs)
        organization = self.request.user.get_organization()
        if organization.is_kind_supplier():
            return ProductDiscount.objects.filter(
                organization=organization, target=target, status__in=["DRAFT", "ACTIVE"]
            )
        elif organization.is_kind_retailer():
            return ProductDiscount.objects.filter(
                organization=target, target=organization, status="ACTIVE"
            )


class PrivateOrganizationPartnersDiscountDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PrivateOrganizationPartnerDiscountSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("discount_uid", None),
        }
        return get_object_or_404(self.queryset, **kwargs)


class PrivatePartnersDiscountList(generics.ListCreateAPIView):
    queryset = ProductDiscount.objects.filter()
    serializer_class = PrivateOrganizationPartnerDiscountSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.get_organization())


class PrivateOrganizationPartnersFileList(generics.ListAPIView):
    queryset = FileItem.objects.filter()
    serializer_class = PrivateOrganizationPartnerFileItemSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {
            "uid": self.kwargs.get("uid", None),
        }
        target = get_object_or_404(Organization.objects.get_status_fair(), **kwargs)
        # Check the logged in user's current organization
        organization = self.request.user.get_organization()
        # Only get the file items that are accessible by the logged in user's current organization
        ids = FileItemAccess.objects.filter(partner=target).values_list(
            "fileitem_id", flat=True
        )
        if organization.is_kind_supplier():
            # If the logged in user's current organization is a supplier
            # and the organization owns the shared files
            return FileItem.objects.filter(
                organization=organization,
                id__in=ids,
                status__in=["DRAFT", "PUBLISHED", "UNPUBLISHED"],
            )
        if organization.is_kind_retailer():
            # If the logged in user's current organization is a retailer
            # and they are not the organization that owns the shared files
            return FileItem.objects.filter(id__in=ids, status="PUBLISHED")


class PrivateBulkCreatePartners(generics.CreateAPIView):
    serializer_class = PrivateBulkCreatePartnersSerializers
    permission_classes = [IsOrganizationStaff]


class PrivateOrganizationPartnerUserList(generics.ListAPIView):
    serializer_class = PrivateOrganizationPartnerUserListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid")
        partner_organization = get_object_or_404(Organization.objects.filter(), uid=uid)
        users = partner_organization.get_users().values_list("user", flat=True)

        return User.objects.filter(id__in=users)
