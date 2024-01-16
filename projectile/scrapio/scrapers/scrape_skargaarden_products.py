import requests
from bs4 import BeautifulSoup
from concurrent import futures
from tqdm import tqdm

from ..models import ScrapProductData

url = "https://www.skargaarden.com/products/"


def scrape(product):
    product_title = product.select_one(".woocommerce-loop-product__title").get_text(
        strip=True
    )
    product_link = product["href"]
    product_description = ""

    description_response = session.get(product_link)
    description_soup = BeautifulSoup(description_response.content, "lxml")
    description = description_soup.select_one(".product-description p")

    if description:
        product_description = description.get_text(strip=True)

    product_image_link = product.select_one("img")["src"]
    product_category = product.select_one(".products-category").get_text()
    product_organization = "Skargaarden"

    return (
        product_title,
        product_description,
        product_image_link,
        product_link,
        product_category,
        product_organization,
    )


def load_data_to_database(list_of_products):
    ScrapProductData.objects.bulk_create(
        [
            ScrapProductData(
                title=item["title"],
                description=item["description"],
                image_link=item["image_link"],
                product_link=item["product_link"],
                category=item["category"],
                organization=item["organization"],
            )
            for item in list_of_products
            if not ScrapProductData.objects.filter(
                product_link=item["product_link"]
            ).exists()
        ]
    )


def main_bot():
    global session
    session = requests.Session()

    products = []

    for i in range(1, 13):
        response = session.get(url + "/page/{}/".format(i))
        soup = BeautifulSoup(response.content, "lxml")
        product_list = soup.select(
            ".woocommerce-LoopProduct-link.woocommerce-loop-product__link"
        )

        products.extend(product_list)

    list_of_products = []

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        products = tqdm(executor.map(scrape, products), total=len(products))

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
    ]

    load_data_to_database(list_of_products)

    session.close()
