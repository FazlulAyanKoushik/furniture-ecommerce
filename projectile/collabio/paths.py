def get_project_image_path(instance, filename):
    return f"projects/{instance.organization_slug}/{instance.slug}/{filename}"
