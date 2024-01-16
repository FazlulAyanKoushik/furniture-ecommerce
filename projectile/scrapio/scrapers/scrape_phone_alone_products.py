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

url = "https://phone-alone.com/products/"

list_of_products = []


# Scraping function for scrape products
def scraping(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    logging.info("Scraping products!")
    for product in tqdm(soup.find_all("a", class_="elementor-cta")):
        product_title = product.find("h6").text
        image_link = (
            product.find("div", class_="elementor-cta__bg")["style"]
            .split("(")[1]
            .split(")")[0]
        )
        product_link = product.get("href")
        organization = urlparse(url).netloc.split(".")[0]
        description_response = requests.get(product_link)
        description_soup = BeautifulSoup(description_response.text, "html.parser")
        for description in description_soup.select(
            "div.elementor-element.elementor-element-dc2afd8.elementor-widget.elementor-widget-text-editor, div.elementor-element.elementor-element-4855f87.elementor-widget.elementor-widget-text-editor"
        ):
            product_description = description.text.strip()

        # Create product dictionary to load data into database
        product_dict = {
            "title": product_title,
            "description": product_description,
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
    ScrapProductData.objects.bulk_create(
        [
            ScrapProductData(
                title=item["title"],
                description=item["description"],
                image_link=item["image_link"],
                product_link=item["product_link"],
                organization=item["organization"],
            )
            for item in tqdm(list_of_products)
            if not ScrapProductData.objects.filter(
                product_link=item["product_link"]
            ).exists()
        ]
    )


# Create a function to call in management command
def main_bot():
    scraping(url)
    load_data_to_database(list_of_products)
