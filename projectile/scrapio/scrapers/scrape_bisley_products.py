import logging
import requests

from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urlparse

from scrapio.models import ScrapProductData


# Initialize the logger
logging.basicConfig(level=logging.INFO)

url_list = [
    "https://www.bisley.com/products/workspace/",
    "https://www.bisley.com/products/storage/",
    "https://www.bisley.com/products/livingbybisley/",
    "https://www.bisley.com/products/belong/",
]

list_of_products = []


# Scraping function for scrape products
def scraping(url):
    response = requests.get(url)
    # Parse the page source using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract information about the products
    product_list = soup.find_all("div", class_="entry-card")
    logging.info("Scraping products!")
    for product in tqdm(product_list):
        base_url = "https://www.bisley.com"
        # Create product dictionary to load data into database
        title = product.find("a", class_="entry-card__banner__title").text.strip()
        description = product.find("p").text.strip()
        image_link = product.find("img")["data-srcset"].split(", ")[-2].split()[0]
        product_link = f"{base_url}" + product.find("a")["href"].strip()
        product_category = product_link.split("/")[4]
        organization = urlparse(base_url).netloc.split(".")[1]

        # Create product dictionary to load data into the database
        product_dict = {
            "title": title,
            "description": description,
            "image_link": image_link,
            "product_link": product_link,
            "category": product_category,
            "organization": organization,
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
