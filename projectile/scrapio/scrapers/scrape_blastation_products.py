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

base_url = "https://www.blastation.com"
url_list = [
    "https://www.blastation.com/products",
    "https://www.blastation.com/products/fittings",
    "https://www.blastation.com/products/for-projects",
]

list_of_products = []


def scraping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select(".product-list li")
    for product in products:
        product_category = product.select_one("h2 a").get_text(strip=True)
        logging.info(product_category)
        product_link = product.select("article")
        for product_detail in tqdm(product_link):
            product_url = base_url + product_detail.find("a")["href"]
            product_title = product_detail.find("h3").text
            product_image = product_detail.select_one("a figure img")
            if product_image:
                if "src" in product_image.attrs:
                    image_url = product_image["src"]
                elif "data-original" in product_image.attrs:
                    image_url = product_image["data-original"]
                else:
                    image_url = None
            product_image_url = base_url + image_url
            organization = urlparse(base_url).netloc.split(".")[1].capitalize()
            detail_response = requests.get(product_url)
            detail_soup = BeautifulSoup(detail_response.text, "html.parser")
            product_description = detail_soup.select_one(".preamble p")
            if product_description:
                description = product_description.get_text(strip=True)
            else:
                description = ""
            # Create product dictionary to load the data into database
            product_dict = {
                "title": product_title,
                "description": description,
                "image_link": product_image_url,
                "product_link": product_url,
                "category": product_category,
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
    for url in url_list:
        scraping(url)
    load_data_to_database(list_of_products)
