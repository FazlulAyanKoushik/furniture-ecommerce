def get_tag_slug(instance):
    if instance.parent:
        return f"{instance.parent.slug}-{instance.name}"
    return f"{instance.category}-{instance.name}"
