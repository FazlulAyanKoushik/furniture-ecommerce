from rest_framework import permissions

from accountio.choices import OrganizationUserRole, OrganizationUserStatus


class IsProjectStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True

        profile = request.user.get_organization_user()
        if profile is not None and profile.status == OrganizationUserStatus.ACTIVE:
            return (
                profile.role
                in [
                    OrganizationUserRole.STAFF,
                    OrganizationUserRole.ADMIN,
                    OrganizationUserRole.OWNER,
                ]
                and profile.organization == object_.project.organization
            )
        return False
