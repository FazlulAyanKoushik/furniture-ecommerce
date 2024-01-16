from django.db import models

from .choices import GroupKind, GroupStatus, MemberRole, MemberStatus


class GroupQuerySet(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=GroupStatus.ACTIVE)

    def get_public_groups(self):
        return self.filter(
            kind__in=[GroupKind.PUBLIC, GroupKind.CLOSED], status=GroupStatus.ACTIVE
        )


class MemberQuerySet(models.QuerySet):
    def get_role_admins(self):
        return self.filter(role=MemberRole.ADMIN)

    def get_role_moderators(self):
        roles = [MemberRole.ADMIN, MemberRole.MODERATOR]
        return self.filter(role__in=roles)

    def get_role_members(self):
        return self.filter(role=MemberRole.MEMBER)

    def get_status_all(self):
        return self.filter()

    def get_status_accepted(self):
        statuses = [MemberStatus.MODERATOR_ACCEPTED, MemberStatus.USER_ACCEPTED]
        return self.filter(status__in=statuses)

    def get_status_rejected(self):
        statuses = [MemberStatus.MODERATOR_REJECTED, MemberStatus.USER_REJECTED]
        return self.filter(status__in=statuses)
