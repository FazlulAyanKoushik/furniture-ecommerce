from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response


from accountio.choices import OrganizationStatus

from weapi.rest.serializers.status import PrivateWeStatusSerializer


class PrivateWeStatusDetail(RetrieveUpdateAPIView):
    """
    Retrieve, update and set status field of organization.
    """

    serializer_class = PrivateWeStatusSerializer
    lookup_field = None

    def get_object(self):
        return self.request.user.get_organization()

    def patch(self, request, format=None):
        we = self.get_object()
        serializer = PrivateWeStatusSerializer(we, data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data["status"]
        if status == OrganizationStatus.PENDING and we.status in [
            OrganizationStatus.DRAFT,
        ]:
            we.set_status_pending()
        return Response(serializer.data)
