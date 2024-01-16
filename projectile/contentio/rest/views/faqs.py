from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from contentio.models import FAQ
from contentio.rest.serializers.faqs import GlobalFAQSerializer


class GlobalFAQList(generics.ListAPIView):
    queryset = FAQ.objects.filter()
    permission_classes = [AllowAny]
    filterset_fields = ["segment"]

    def get(self, request):
        segment = self.request.query_params.get("segment", None)
        queryset = self.queryset.filter(segment="FAQ")
        if segment is not None:
            queryset = self.queryset.filter(segment=segment)

        queryset = queryset.order_by("-created_at")

        faq_dict = {}
        for faq in queryset:
            category = faq.category
            faq_data = GlobalFAQSerializer(faq).data
            if category not in faq_dict:
                faq_dict[category] = []
            faq_dict[category].append(faq_data)

        # Convert the dictionary to a list of dictionaries containing category and FAQs
        faq_list = [
            {"category": category, "faqs": faqs} for category, faqs in faq_dict.items()
        ]

        return Response(faq_list, status=status.HTTP_200_OK)


class GlobalFAQDetail(generics.RetrieveAPIView):
    queryset = FAQ.objects.filter()
    serializer_class = GlobalFAQSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
