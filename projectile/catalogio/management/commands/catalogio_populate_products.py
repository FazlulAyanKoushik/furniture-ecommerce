import logging
import os
import json

from django.core.management.base import BaseCommand

from tqdm import tqdm
from io import BytesIO

import requests
from django.core.files.base import ContentFile
from PIL import Image

from accountio.models import Organization
from catalogio.models import Product, ProductBrand

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

logger = logging.getLogger(__name__)


def is_image(url):
    return (
        url.endswith(".jpg")
        or url.endswith(".jpeg")
        or url.endswith(".png")
        or url.endswith(".webp")
    )


def get_category(url):
    url = url.lower()
    if url == "" or url is None:
        return ""
    if "table" in url:
        return "product-table-others"
    if "chair" in url:
        return "product-seating-chair"
    if "barstool" in url:
        return "product-seating-barstool"
    return ""


def fetch_and_set_image(url, model):
    response = requests.get(url)

    if response.status_code == 200 and is_image(url):
        try:
            with Image.open(ContentFile(response.content)) as im:
                if im.mode == "RGBA":
                    # Convert the image to JPG with a white background
                    output = BytesIO()
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    bg.paste(im, mask=im.split()[3])
                    bg.save(output, "JPEG", quality=95)
                    output.seek(0)
                    content = output.getvalue()
                else:
                    # Use the original image data
                    content = response.content
                if content:
                    file_name = url.split("/")[-1]
                    model.image.save(file_name, ContentFile(content), save=True)
                    logger.info(f'Successfully downloaded and saved image from "{url}"')
        except Exception as e:
            logger.exception(e)
    else:
        logger.info(f'Failed to download image from "{url}"')


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        path = os.path.abspath(os.path.dirname(__file__))
        file_ = open(f"{path}/data.json")

        # returns JSON object as
        # a dictionary
        data = json.load(file_)
        for item in tqdm(data["results"]):
            if Product.objects.filter(external_url=item["product_link"]).exists():
                continue

            try:
                organization_name = item["organization"]["name"]
                try:
                    organization = Organization.objects.get(
                        name__contains=organization_name
                    )
                except Organization.DoesNotExist as e:
                    organization = Organization()
                    organization.name = organization_name
                    organization.registration_no = f"{organization_name}-123456"
                    organization.display_name = organization_name.replace(" AB", "")
                    organization.save()

                brand_name = item["organization"].get(
                    "name", item["organization"]["name"]
                )
                try:
                    brand = ProductBrand.objects.get(title__icontains=brand_name)
                except ProductBrand.DoesNotExist as e:
                    brand = ProductBrand()
                    brand.title = brand_name
                    brand.organization = organization
                    brand.save()

                product = Product()
                product.organization = organization
                product.brand = brand
                product.title = item["title"]
                product.description = item["description"]
                product.external_url = item["product_link"]
                product.status = "DRAFT"
                product.scraped = item

                product.category = get_category(item["product_link"])

                product.save()

                if item["images"]:
                    fetch_and_set_image(item["images"][0]["image_url"], product)
                    continue

            except Exception as e:
                logger.exception(e)
                logger.info(item)
                continue
