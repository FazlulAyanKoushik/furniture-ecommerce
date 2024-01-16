import concurrent.futures
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import urllib.parse

from ..models import ScrapProductData

url = "https://www.hermanmiller.com/en_us"


def scrape(product):
    product_title = product.select_one(".product-name").get_text()
    image_link = product.select_one(".first")["src"]
    product_image_link = "https://www.hermanmiller.com/{}".format(image_link)
    product_link = product["href"]

    parsed_url = urllib.parse.urlparse(product_link)
    path = parsed_url.path

    product_category = path.split("/")[-2].replace("-", " ").title()
    product_organization = "Herman Miller"
    product_description = ""

    description_response = session.get(product_link)
    description_soup = BeautifulSoup(description_response.content, "lxml")
    description = description_soup.select(".text-body-1")

    if description:
        product_description = description[0].text

    return (
        product_title,
        product_description,
        product_image_link,
        product_link,
        product_category,
        product_organization,
    )


def load_data_to_database(list_of_products):
    existing_product_links = ScrapProductData.objects.values_list(
        "product_link", flat=True
    )
    existing_image_links = ScrapProductData.objects.values_list("image_link", flat=True)

    new_products = []
    for product in list_of_products:
        if (
            product["product_link"] not in existing_product_links
            and product["image_link"] not in existing_image_links
        ):
            new_products.append(
                ScrapProductData(
                    title=product["title"],
                    description=product["description"],
                    image_link=product["image_link"],
                    product_link=product["product_link"],
                    category=product["category"],
                    organization=product["organization"],
                )
            )
        else:
            print(f"Product already exists: {product['product_link']}")

    tqdm_products = tqdm(new_products, total=len(new_products))
    ScrapProductData.objects.bulk_create(tqdm_products)


def main_bot():
    global session
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    product_list = soup.select(
        "ul.navigation-root.navigation-branch.navigation-level2 li a"
    )

    for product in product_list:
        if product["href"].startswith(
            "https://www.hermanmiller.com/products/"
        ) and not product["title"].startswith("All"):
            product_response = session.get(product["href"])
            product_soup = BeautifulSoup(product_response.content, "lxml")

            products = product_soup.select(".product-grid-element a")

            list_of_products = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                products = executor.map(scrape, products)
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
