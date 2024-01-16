from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny
from rest_framework import filters, generics, status
from rest_framework.response import Response

from accountio.models import OrganizationUser
from accountio.rest.permissions import IsOrganizationStaff

from ..serializers import users as organization_users

User = get_user_model()


class PrivateOrganizationUserList(generics.ListCreateAPIView):
    queryset = OrganizationUser.objects.get_status_editable()
    serializer_class = organization_users.PrivateOrganizationUserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["user__first_name", "user__last_name"]
    ordering_fields = ["user__first_name", "user__last_name", "created_at", "user__last_login"]

    def get_queryset(self):
        organization = self.request.user.get_organization()
        return self.queryset.filter(organization=organization)


class PrivateOrganizationUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrganizationUser.objects.get_status_editable()
    serializer_class = organization_users.PrivateOrganizationUserSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("uid", None)}
        return get_object_or_404(OrganizationUser, **kwargs)


class PrivateOrganizationUserSetPassword(generics.UpdateAPIView):
    serializer_class = organization_users.PrivateOrganizationUserSetPasswordSerializer
    permission_classes = [AllowAny]

    def update(self, request, *args, **kwargs):
        token = self.kwargs.get("token")

        # Get organization user
        organization_user = get_object_or_404(
            User.objects.filter(profiles__token=token)
        )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Get password and confirm password from user
            password = request.data.get("password")
            confirm_password = request.data.get("confirm_password")

            # Checking passwords are same
            if password != confirm_password:
                response = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "error": "Password not matched.",
                }
                return Response(response)

            # Save user password
            organization_user.set_password(password)
            organization_user.save()

            response = {
                "status": status.HTTP_200_OK,
                "message": "Password changed successfully",
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
