from rest_framework import permissions

from ..choices import OrganizationUserRole, OrganizationUserStatus


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
                    and profile.organization == object_
                )
        return False


class IsOrganizationAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_active:
            profile = user.get_organization_user()
            if profile.status == OrganizationUserStatus.ACTIVE:
                return (
                    profile.role
                    in [
                        OrganizationUserRole.ADMIN,
                        OrganizationUserRole.OWNER,
                    ]
                    and profile.organization == object_
                )
        return False


class IsOrganizationOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_active:
            profile = user.get_organization_user()
            if profile.status == OrganizationUserStatus.ACTIVE:
                return (
                    profile.role
                    in [
                        OrganizationUserRole.OWNER,
                    ]
                    and profile.organization == object_
                )
        return False


class IsSameUser(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, object_):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user`.
        return object_.user == request.user
