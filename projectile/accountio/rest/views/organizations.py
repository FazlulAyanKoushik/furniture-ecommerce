from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from ...models import Organization
from ..serializers import organizations
from ..serializers import organizations, onboarding


class PublicOrganizationOnboardingDetail(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = onboarding.PublicOrganizationUserOnboardingSerializer(
            data=request.data, context = {"request":request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(True, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicOrganizationList(generics.ListAPIView):
    queryset = Organization.objects.get_status_fair()
    serializer_class = organizations.PublicOrganizationListSerializer
    filterset_fields = ("name", "kind")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset.order_by("name")
        return queryset


class PublicOrganizationDetail(generics.RetrieveAPIView):
    queryset = Organization.objects.get_status_fair()
    serializer_class = organizations.PublicOrganizationDetailSerializer
    
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]


class PublicOrganizationListByProject(generics.ListAPIView):
    queryset = Organization.objects.get_status_fair()
    serializer_class = organizations.PublicOrganizationListSerializer
    filterset_fields = ("name", "kind")
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset.filter(project__isnull=False).order_by("name")
        return queryset
