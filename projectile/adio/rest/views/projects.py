from rest_framework import generics
from rest_framework.permissions import AllowAny

from adio.models import AdProject
from ..serializers.projects import GlobalProjectAdSerializer


class GlobalProjectAdList(generics.ListAPIView):
    queryset = AdProject.objects.get_status_active().order_by("?")[:4]
    serializer_class = GlobalProjectAdSerializer
    permission_classes = [AllowAny]


class GlobalProjectAdDetail(generics.RetrieveAPIView):
    serializer_class = GlobalProjectAdSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs.get("slug", None)
        ad_project = generics.get_object_or_404(AdProject.objects.get_status_active(), slug=slug)
        ad_project.increment_count()
        return ad_project
