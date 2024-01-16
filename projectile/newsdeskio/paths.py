def get_newsdeskpost_image_path(instance, filename):
    return f"organization/{instance.organization_slug}/newsdeskposts/{instance.slug}/{filename}"
