from rest_framework.generics import RetrieveUpdateAPIView

from ..serializers.we import PrivateWeOrganizationSerializer


class PrivateWeDetail(RetrieveUpdateAPIView):
    """
    Retrieve, update or delete a the selected
    organization for logged in user.
    """

    serializer_class = PrivateWeOrganizationSerializer

    def get_object(self):
        return self.request.user.get_organization()
