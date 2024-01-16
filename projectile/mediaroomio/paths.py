def get_mediaimage_image_path(instance, filename):
    return f"{instance.organization.slug}/mediaimages/{instance.uid}/{filename}"
