def get_fileitem_file_path(instance, filename):
    return f"{instance.organization.slug}/files/{instance.uid}/{filename}"
