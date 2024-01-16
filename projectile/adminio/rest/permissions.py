from rest_framework import permissions


class IsStaff(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        if user.is_staff and user.is_active:
            return True

        return False
