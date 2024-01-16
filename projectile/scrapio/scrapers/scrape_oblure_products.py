import logging
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse

from scrapio.models import ScrapProductData


# Initialize the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

base_url = "https://oblure.com"
url = "https://oblure.com/products/"

list_of_products = []


def scraping(url):
    # Navigate to the website
    response = requests.get(url)
    # Get the page source and create a BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    product_link = soup.find_all(
        "a", class_="vc_single_image-wrapper vc_box_border_grey"
    )

    unique_links = set()

    for product in product_link:
        if product:
            product_link = product.get("href")
            if product_link.startswith("/"):
                product_url = base_url + product_link
            else:
                product_url = product_link
            unique_links.add(product_url)

    for product_link in tqdm(unique_links):
        product_detail_response = requests.get(product_link)
        product_detail_soup = BeautifulSoup(product_detail_response.text, "html.parser")
        product_title = product_detail_soup.find(
            "h1", class_="product_title entry-title"
        ).get_text()
        image_link = product_detail_soup.find(
            "img", class_="attachment-shop_single size-shop_single wp-post-image"
        )
        if image_link is not None:
            image_link = image_link["src"]
        product_description = product_detail_soup.select(
            ".wpb_text_column.wpb_content_element  div p"
        )
        description = (
            product_description[0].text.strip()
            + " "
            + product_description[1].text.strip()
        )
        organization = urlparse(base_url).netloc.split(".")[0]

        # Create product dictionary to load the data into database
        product_dict = {
            "title": product_title,
            "description": description,
            "image_link": image_link,
            "product_link": product_link,
            "organization": organization,
        }
        list_of_products.append(product_dict)


# Load the scraped data into the database
def load_data_to_database(list_of_products):
    logging.info(
        "Loading scraped products into the database if the same product does not exist!"
    )
    existing_product_links = ScrapProductData.objects.values_list(
        "product_link", flat=True
    )
    existing_image_links = ScrapProductData.objects.values_list("image_link", flat=True)

    new_products = []
    num_new_products = 0

    for item in list_of_products:
        if (
            item["product_link"] not in existing_product_links
            and item["image_link"] not in existing_image_links
        ):
            new_products.append(
                ScrapProductData(
                    title=item["title"],
                    description=item["description"],
                    image_link=item["image_link"],
                    product_link=item["product_link"],
                    organization=item["organization"],
                )
            )
            num_new_products += 1
        else:
            logging.warning(f"Product already exists: {item['product_link']}")

    tqdm_new_products = tqdm(new_products, total=num_new_products)

    ScrapProductData.objects.bulk_create(tqdm_new_products)


# Create a function to call in management command
def main_bot():
    scraping(url)
    load_data_to_database(list_of_products)
