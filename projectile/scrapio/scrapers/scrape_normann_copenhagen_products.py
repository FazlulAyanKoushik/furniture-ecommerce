import logging
import requests
from bs4 import BeautifulSoup
from concurrent import futures
from tqdm import tqdm

from ..models import ScrapProductData

# Initialize the logger
logging.basicConfig(level=logging.INFO)

urls = [
    "https://www.normann-copenhagen.com/en/Products/Furniture?page=30",
    "https://www.normann-copenhagen.com/en/Products/Lighting?page=4",
    "https://www.normann-copenhagen.com/en/Products/Accessories?page=12",
]


def scrape(product):
    if product.select_one(".header"):
        title = product.select_one(".header").get_text(strip=True)
        description = ""
        image_link = (
            "https://www.normann-copenhagen.com"
            + product.select_one(".canvas img")["src"]
        )
        product_link = "https://www.normann-copenhagen.com" + product["href"]
        category = product_link.split("/")[6]
        organization = "Normann Copenhagen"

        description_response = session.get(product_link)
        description_soup = BeautifulSoup(description_response.content, "lxml")
        product_description = description_soup.select_one(".contentSection")

        if product_description:
            description = product_description.get_text(strip=True)

        return (title, description, image_link, product_link, category, organization)


def load_data_to_database(list_of_products):
    logging.info(
        "Loading scraped products into the database if the same product does not exist!"
    )
    existing_product_links = ScrapProductData.objects.values_list(
        "product_link", flat=True
    )
    existing_image_links = ScrapProductData.objects.values_list("image_link", flat=True)

    products = []
    for item in list_of_products:
        if (
            item["product_link"] not in existing_product_links
            and item["image_link"] not in existing_image_links
        ):
            products.append(
                ScrapProductData(
                    title=item["title"],
                    description=item["description"],
                    image_link=item["image_link"],
                    product_link=item["product_link"],
                    category=item["category"],
                    organization=item["organization"],
                )
            )
        else:
            logging.warning(f"Product already exists: {item['product_link']}")

    tqdm_products = tqdm(products, total=len(products))
    ScrapProductData.objects.bulk_create(tqdm_products)


def main_bot():
    global session
    session = requests.Session()

    for url in urls:
        response = session.get(url)

        soup = BeautifulSoup(response.content, "lxml")

        product_list = soup.select(
            ".clearfix.basicspot.masonryItem.Product.grid-wrapper-heavy a"
        )
        list_of_products = []

        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            products = executor.map(scrape, product_list)

        list_of_products = [
            {
                "title": product[0],
                "description": product[1],
                "image_link": product[2],
                "product_link": product[3],
                "category": product[4],
                "organization": product[5],
            }
            for product in products
            if not product == None
        ]

        load_data_to_database(list_of_products)

    session.close()
