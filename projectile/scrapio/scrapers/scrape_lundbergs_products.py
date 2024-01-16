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

base_url = "https://www.lundbergs-mobler.se"
url = "https://www.lundbergs-mobler.se/kollektion"

list_of_products = []


def scraping(url):
    # Navigate to the website
    response = requests.get(url)

    # Get the page source and create a BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.select(".standard-btn")[2:7]
    # Get categories
    for category in categories:
        logging.info(category.text.strip())
        category_name = category.get_text(strip=True)
        organization = urlparse(base_url).netloc.split(".")[1]
        category_link = base_url + category["href"]
        category_response = requests.get(category_link)
        product_soup = BeautifulSoup(category_response.text, "html.parser")
        products = product_soup.select(".grid-image")
        # Get all product details
        for product in tqdm(products):
            product_link = base_url + product.select_one("a[href]")["href"]
            product_detail = requests.get(product_link)
            product_detail_soup = BeautifulSoup(product_detail.text, "html.parser")
            product_image_link = product_detail_soup.select_one("img")["src"]
            product_title = product_detail_soup.select_one(
                "h1",
                class_="size-xl font-family-label font-weight-bold fade-left inview",
            ).get_text(strip=True)
            product_description = product_detail_soup.select_one(
                ".right.col-13.col-mdtablet-24.m-mdtablet-t-3 div div p"
            ).get_text(strip=True)

            # Create product dictionary to load the data into database
            product_dict = {
                "title": product_title,
                "description": product_description,
                "image_link": product_image_link,
                "product_link": product_link,
                "category": category_name,
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
                    category=item["category"],
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
