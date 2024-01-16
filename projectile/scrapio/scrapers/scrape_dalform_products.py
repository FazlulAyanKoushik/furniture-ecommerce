import logging
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm

from ..models import ScrapProductData


# Initialize the logger
logging.basicConfig(level=logging.INFO)

url_list = [
    "https://dalform.se/produktkategori/produkter/skap/alla-skap/",
    "https://dalform.se/produktkategori/produkter/kapprumsinredning/",
    "https://dalform.se/produktkategori/produkter/bankar-kroklister/",
]

list_of_products = []


# Scraping function for scrape products
def scraping(url):
    response = requests.get(url)
    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    product_category = soup.find("header", class_="woocommerce-products-header")
    category = product_category.find("h1").text.strip()
    product_data = soup.find_all("div", class_="nv-card-content-wrapper")
    # Get products data
    for product in tqdm(product_data):
        product_link = product.find("a", class_="sp-product-overlay-link")[
            "href"
        ].strip()
        product_title = product.find("h2").text.strip()
        product_description = ""
        description_response = requests.get(product_link)
        description_soup = BeautifulSoup(description_response.text, "html.parser")
        all_description = description_soup.find_all(
            "div", class_="woocommerce-product-details__short-description"
        )
        if all_description:
            product_description = all_description[0].text.strip()
        product_image_link = description_soup.find(
            "figure", class_="woocommerce-product-gallery__wrapper"
        )
        image_link = product_image_link.find_all("a")[0]["href"]
        organization = description_soup.find("a", class_="brand")["title"]

        # Create product dictionary to load data into database
        product_dict = {
            "title": product_title,
            "description": product_description,
            "image_link": image_link,
            "product_link": product_link,
            "organization": organization,
            "category": category,
        }
        # Append data into the list_of_products
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
                    category=item["category"],
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
