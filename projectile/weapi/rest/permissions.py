from rest_framework import permissions

from accountio.choices import OrganizationUserRole, OrganizationUserStatus

from catalogio.models import Service, OrganizationServiceConnector

from gruppio.models import Group

from tagio.models import Tag, TagConnector


class IsOrganizationDefaultStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        profile = user.get_organization_user()
        if profile is not None and profile.status == OrganizationUserStatus.ACTIVE:
            return profile.role in [
                OrganizationUserRole.STAFF,
                OrganizationUserRole.ADMIN,
                OrganizationUserRole.OWNER,
            ]
        return False


class IsTagConnectorOrganizationStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Tag):
            user = request.user
            if user.is_active:
                profile = user.get_organization_user()
                if (
                    profile is not None
                    and profile.status == OrganizationUserStatus.ACTIVE
                ):
                    tag_connector_exists = TagConnector.objects.filter(
                        organization=profile.organization,
                        tag=obj,
                    ).exists()

                    return tag_connector_exists and profile.role in [
                        OrganizationUserRole.STAFF,
                        OrganizationUserRole.ADMIN,
                        OrganizationUserRole.OWNER,
                    ]
        return False


class IsOrganizationServiceConnectorStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Service):
            user = request.user
            if user.is_active:
                profile = user.get_organization_user()
                if (
                    profile is not None
                    and profile.status == OrganizationUserStatus.ACTIVE
                ):
                    service_connector_exists = (
                        OrganizationServiceConnector.objects.filter(
                            organization=profile.organization,
                            service=obj,
                        ).exists()
                    )

                    return service_connector_exists and profile.role in [
                        OrganizationUserRole.STAFF,
                        OrganizationUserRole.ADMIN,
                        OrganizationUserRole.OWNER,
                    ]
        return False


class IsGroupOrganizationStaff(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        if request.method in permissions.SAFE_METHODS:
            return True

        group_uid = view.kwargs.get("group_uid", None)

        if group_uid is not None:
            user = request.user
            if user.is_active:
                profile = user.get_organization_user()
                if (
                    profile is not None
                    and profile.status == OrganizationUserStatus.ACTIVE
                ):
                    try:
                        group = Group.objects.get(
                            uid=group_uid, organization=profile.organization
                        )
                    except Group.DoesNotExist:
                        return False

                    return (
                        profile.role
                        in [
                            OrganizationUserRole.STAFF,
                            OrganizationUserRole.ADMIN,
                            OrganizationUserRole.OWNER,
                        ]
                        and profile.organization == group.organization
                    )

        return False
