from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from invitio.models import OrganizationInvite
from invitio.helpers.emails import send_connect_email

from ..serializers import organization_invitation
from ..permissions import IsOrganizationStaff


class PublicOrganizationPartnerInvitation(generics.CreateAPIView):
    queryset = OrganizationInvite.objects.filter()
    permission_classes = [IsOrganizationStaff]
    serializer_class = organization_invitation.PublicPartnerInviteSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["slug"] = self.kwargs.get("slug", None)
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(
            data=request.data, context={"request": request, "slug": kwargs.get("slug")}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        send_connect_email(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
