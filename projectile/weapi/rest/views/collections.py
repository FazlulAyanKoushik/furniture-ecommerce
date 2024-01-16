from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.response import Response

from catalogio.models import (
    ProductCollection,
    ProductCollectionBridge,
    Product,
)
from catalogio.rest.permissions import IsOrganizationStaff

from ..serializers import collections, products


class PrivateOrganizationCollection(generics.ListCreateAPIView):
    """View for serving collection list for a organization"""

    queryset = ProductCollection.objects.filter()
    serializer_class = collections.PrivateOrganizationCollectionListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateOrganizationCollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for serving collection list for a organization"""

    queryset = ProductCollection.objects.filter()
    serializer_class = collections.PrivateOrganizationCollectionDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}  
        return get_object_or_404(ProductCollection, **kwargs)


class PrivateCollectionProductList(views.APIView):
    permission_classes = [IsOrganizationStaff]

    def get(self, request, format=None, **kwargs):
        collection = ProductCollection.objects.get(uid=kwargs["uid"])
        products_ids = collection.productcollectionbridge_set.filter().values_list(
            "product_id", flat=True
        )
        products_list = Product.objects.filter(id__in=products_ids)
        serializer = products.PrivateProductListSerializer(
            data=products_list, many=True
        )
        serializer.is_valid()
        return Response(serializer.data)

    def post(self, request, format=None, **kwargs):
        serializer = collections.PrivateCollectionProducts(
            data=request.data, context={"collection_uid": kwargs["uid"]}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(True, status=status.HTTP_201_CREATED)

    def patch(self, request, format=None, **kwargs):
        """
        The patch is doing the deletion as we trying to take list of uids to delete
        multiple items at once. Couldn't find a way to pass them in the delete request
        and we are not providing patch method with this feature
        """
        # TO DO: Find a way to make the delete happen by delete request

        # validating UUID
        serializer = collections.PrivateCollectionProducts(data=request.data)
        serializer.is_valid(raise_exception=True)
        ProductCollectionBridge.objects.filter(
            collection__uid=kwargs["uid"],
            product__uid__in=request.data["product_uids"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
