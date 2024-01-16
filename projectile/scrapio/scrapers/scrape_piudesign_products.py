import logging
import requests

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib.parse import urlparse

from scrapio.models import ScrapProductData


# Initialize the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Use a ThreadPoolExecutor for concurrent requests
executor = ThreadPoolExecutor()

base_url = "https://piudesign.se"
url = "https://piudesign.se/products/"

list_of_products = []


# Scrape products description
def scrape_product_details(product_link):
    response = session.get(product_link)
    soup = BeautifulSoup(response.text, "html.parser")
    product_description = soup.select(
        ".styles_contentContainer__lrPIa.textnormal.styles_text__3jGMu p"
    )
    description = product_description[2].get_text(strip=True) + product_description[
        3
    ].get_text(strip=True)
    return description


# Scrape products data
def scrape_category(category):
    category_link = base_url + category.select_one("a")["href"]
    category_name = category.select_one("p span").text
    logging.info(category_name)
    if category_link == "https://piudesign.se/products/acoustic/calm-studio":
        return None

    category_response = session.get(category_link)
    category_soup = BeautifulSoup(category_response.text, "html.parser")
    products = category_soup.select(".Gallery_galleryCell__2ARa3.gallery-cell")
    for product in products:
        product_link = product.select_one("a")
        if not product_link or "href" not in product_link.attrs:
            continue
        product_link = base_url + product_link["href"]
        product_title = product.select_one("p span").text
        image_link = (
            base_url + product.select_one("img")["srcset"].split(", ")[-1].split()[0]
        )
        organization = urlparse(base_url).netloc.split(".")[0].capitalize()

        # Schedule the product details scraping using ThreadPoolExecutor
        future = executor.submit(scrape_product_details, product_link)

        # Create product dictionary to load the data into the database
        product_dict = {
            "title": product_title,
            "description": None,  # Placeholder for the description
            "image_link": image_link,
            "product_link": product_link,
            "category": category_name,
            "organization": organization,
            "future": future,  # Store the future object for retrieving the description later
        }

        list_of_products.append(product_dict)


def load_data_to_database():
    # Retrieve the product descriptions from the completed futures
    for item in list_of_products:
        item["description"] = item["future"].result()

    logging.info(
        "Loading scraped products into the database if the same product does not exist!"
    )
    existing_product_links = ScrapProductData.objects.values_list(
        "product_link", flat=True
    )

    new_products = []
    num_new_products = 0

    for item in list_of_products:
        if item["product_link"] not in existing_product_links:
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


def main_bot():
    global session, list_of_products

    # Create a session object for making requests
    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_category = soup.select(".Gallery_galleryCell__2ARa3.gallery-cell")

    # Scrape categories concurrently using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(scrape_category, all_category)

    load_data_to_database()
