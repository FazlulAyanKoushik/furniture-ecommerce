from uuid import uuid4


def get_brand_image_path(instance, filename):
    uid = str(uuid4()).split("-")[-1]
    return f"{instance.organization.slug}/brands/{instance.slug}/{uid}-{filename}"


def get_product_image_path(instance, filename):
    uid = str(uuid4()).split("-")[-1]
    return f"{instance.organization.slug}/products/{instance.slug}/{uid}-{filename}"


def get_productimage_image_path(instance, filename):
    uid = str(uuid4()).split("-")[-1]
    return f"{instance.organization.slug}/products/{instance.product.slug}/images/{uid}-{filename}"


def get_productcollection_image_path(instance, filename):
    uid = str(uuid4()).split("-")[-1]
    return f"{instance.organization.slug}/collections/{instance.slug}/{uid}-{filename}"


def get_producmaterial_image_path(instance, filename):
    uid = str(uuid4()).split("-")[-1]
    return f"{instance.organization.slug}/products/material/{uid}-{filename}"
