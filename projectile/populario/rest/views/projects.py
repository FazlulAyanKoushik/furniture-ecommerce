from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework.permissions import AllowAny

from collabio.models import Project

from populario.models import PopularProject
from populario.rest.serializers.projects import GlobalProjectSlimSerializer


class GlobalPopularProjectList(generics.ListAPIView):
    queryset = Project.objects.get_popular()[:16]
    serializer_class = GlobalProjectSlimSerializer
    permission_classes = [AllowAny]

    # Cache page for the requested url
    @method_decorator(cache_page(60))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class GlobalPopularProjectDetail(generics.RetrieveAPIView):
    queryset = Project.objects.get_visibility_global()
    serializer_class = GlobalProjectSlimSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"
