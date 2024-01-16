from rest_framework import permissions

from accountio.choices import OrganizationUserRole, OrganizationUserStatus


class IsOrganizationStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_active:
            profile = user.get_organization_user()
            if profile is not None and profile.status == OrganizationUserStatus.ACTIVE:
                return (
                    profile.role
                    in [
                        OrganizationUserRole.STAFF,
                        OrganizationUserRole.ADMIN,
                        OrganizationUserRole.OWNER,
                    ]
                    and profile.organization == object_.organization
                )
        return False
