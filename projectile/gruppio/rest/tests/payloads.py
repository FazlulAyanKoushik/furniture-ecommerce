from gruppio.choices import MemberRole, MemberStatus


def create_group():
    """payload(dict) for a group"""
    payload = {
        "name": "Tech Giants",
        "description": "Groups tech giants oranizations",
    }
    return payload


def create_second_instance_of_group():
    """payload(dict) for group"""
    payload = {
        "name": "Fighters",
        "description": "Groups Fighters oranizations",
    }
    return payload


def create_member(group_id, user):
    """payload(dict) for a member"""
    payload = {
        "group": group_id,
        "user": user.id,
        "role": MemberRole.MEMBER,
        "status": MemberStatus.USER_ACCEPTED,
    }
    return payload
