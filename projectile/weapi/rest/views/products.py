from rest_framework import filters, generics, status
from rest_framework.response import Response

from catalogio.choices import ProductStatus
from catalogio.models import Product, ProductView
from catalogio.rest.permissions import IsOrganizationStaff

from fileroomio.models import FileItem

from mediaroomio.models import MediaImage

from tagio.models import Tag

from ..serializers import products
from ..serializers.products import PrivateProductCoverImageDetailSerializer


class PrivateProductList(generics.ListCreateAPIView):
    queryset = Product.objects.get_status_editable()
    serializer_class = products.PrivateProductListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title"]

    ordering_fields = ["title", "created_at", "updated_at", "view_count"]

    def get_queryset(self):
        return self.queryset.filter(organization=self.request.user.get_organization())


class PrivateProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.get_status_editable()
    serializer_class = products.PrivateProductDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        product = generics.get_object_or_404(Product.objects.filter(), **kwargs)
        product.view_count += 1
        product.save()
        ProductView.objects.create(
            ip_address=self.request.META.get("REMOTE_ADDR"),
            organization=self.request.user.get_organization(),
            product=product,
        )
        return product

    def perform_destroy(self, instance):
        instance.status = ProductStatus.REMOVED
        instance.save()


class PrivateProductImageList(generics.ListCreateAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = products.PrivateProductImageListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        uid = self.kwargs.get("uid", None)
        product = generics.get_object_or_404(Product.objects.get_status_active(), uid = uid)
        image_ids = product.mediaimageconnector_set.filter().values_list(
            "image_id", flat=True
        )
        queryset = self.queryset.filter(id__in=image_ids)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        uid = self.kwargs.get("uid", None)
        product = generics.get_object_or_404(Product.objects.get_status_active(), uid = uid)
        cover_image = queryset.filter(image=product.image ).first()
        data = {
                "cover_image": products.PrivateProductImageListSerializer(cover_image).data if cover_image else {},
                "images": products.PrivateProductImageListSerializer(queryset, many=True).data,
            }
        return Response(data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProductImageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MediaImage.objects.get_kind_image()
    serializer_class = products.PrivateProductImageDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("image_uid", None)}
        return generics.get_object_or_404(MediaImage.objects.filter(), **kwargs)


class PrivateProductFileList(generics.ListCreateAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = products.PrivateProductFileListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        product = generics.get_object_or_404(Product.objects.filter(), **kwargs)
        fileitem_ids = product.fileitemconnector_set.filter().values_list(
            "fileitem_id", flat=True
        )
        return self.queryset.filter(id__in=fileitem_ids)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["uid"] = self.kwargs.get("uid", None)
        return context


class PrivateProductFileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileItem.objects.get_status_editable()
    serializer_class = products.PrivateProductFileDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("file_uid", None)}
        return generics.get_object_or_404(FileItem.objects.filter(), **kwargs)


class PrivateProductTagDetail(generics.RetrieveUpdateAPIView):
    queryset = (
        Tag.objects.filter()
    )  # TODO: need to new query manager (get_status_editable())
    serializer_class = products.PrivateProductTagDetailSerializer
    permission_classes = []

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("tag_uid", None)}
        return generics.get_object_or_404(Tag.objects.filter(), **kwargs)


class PrivateProductCoverImageDetail(generics.UpdateAPIView):
    serializer_class = PrivateProductCoverImageDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("image_uid", None)}
        return generics.get_object_or_404(MediaImage.objects.filter(), **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        product_uid = self.kwargs.get("uid", None)
        product = generics.get_object_or_404(
            Product.objects.get_status_active(), uid=product_uid
        )
        product.image = instance.image
        product.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
