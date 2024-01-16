import logging

logger = logging.getLogger(__name__)


def get_newsdeskpost_slug(instance):
    return f"{instance.organization.slug}-{instance.title}"


def get_newsdeskpost_organization_slug(instance):
    return f"{instance.organization.slug}"
