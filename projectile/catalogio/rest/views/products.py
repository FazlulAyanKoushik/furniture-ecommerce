from django.shortcuts import get_object_or_404

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from fileroomio.models import FileItem

from mediaroomio.models import MediaImage

from ...choices import ProductCollectionVisibility, ProductStatus
from ...models import Product, ProductCollection
from ..permissions import IsOrganizationStaff
from ..serializers import products


class GlobalProductList(generics.ListAPIView):
    queryset = Product.objects.filter(status=ProductStatus.PUBLISHED)
    serializer_class = products.GlobalProductListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["title", "created_at", "updated_at"]


class GlobalProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(status=ProductStatus.PUBLISHED)
    serializer_class = products.GlobalProductDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


class GlobalProductImageList(generics.ListAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = products.GlobalProductImageListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        product = get_object_or_404(Product.objects.filter(), slug=slug)
        image_ids = product.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        return self.queryset.filter(id__in=image_ids)


class GlobalProductImageDetail(generics.RetrieveAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = products.GlobalProductImageDetailSerializer

    def get_object(self):
        uid = self.kwargs.get("image_uid")
        kwargs = {
            "mediaimageconnector__product__slug": self.kwargs.get("product_slug"),
            "uid": uid,
        }

        return get_object_or_404(MediaImage.objects.filter(), **kwargs)


class GlobalProductCollectionList(generics.ListAPIView):
    queryset = ProductCollection.objects.filter(
        visibility=ProductCollectionVisibility.PUBLIC
    )
    serializer_class = products.GlobalProductCollectionListSerializer


class GlobalProductCollectionDetail(generics.RetrieveAPIView):
    queryset = ProductCollection.objects.filter(
        visibility=ProductCollectionVisibility.PUBLIC
    )
    serializer_class = products.GlobalProductCollectionDetailSerializer
    lookup_field = "slug"


class GlobalCollectionProductList(generics.ListAPIView):
    # views class for product collection product list
    queryset = Product.objects.filter(status=ProductStatus.PUBLISHED)
    serializer_class = products.GlobalCollectionProductListSerializer

    # collection slug
    def get_queryset(self):
        collection_slug = ProductCollection.objects.get(slug=self.kwargs["slug"])
        products_ids = collection_slug.productcollectionbridge_set.filter().values_list(
            "product_id", flat=True
        )
        return self.queryset.filter(id__in=products_ids)


class GlobalProductFileList(generics.ListAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = products.GlobalProductFileListSerializer

    def get_queryset(self):
        kwargs = {"slug": self.kwargs.get("slug", None)}
        product = get_object_or_404(Product.objects.filter(), **kwargs)
        fileitem_ids = product.fileitemconnector_set.filter().values_list(
            "fileitem_id", flat=True
        )
        return self.queryset.filter(id__in=fileitem_ids)
