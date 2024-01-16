import requests
from bs4 import BeautifulSoup
from concurrent import futures
from tqdm import tqdm

from ..models import ScrapProductData

url = "https://www.essem.se/sv/produkter"


def scrape(product, image):
    product_title = product.select_one(".product-item-name a h3").get_text(strip=True)
    product_image_link = image.select_one("a img")["src"]
    product_link = "https://www.essem.se" + product.select_one("a")["href"]
    product_organization = "Essem"

    detail_response = session.get(product_link)
    detail_soup = BeautifulSoup(detail_response.content, "lxml")

    product_detail_list = detail_soup.select(".breadcrumbs-container ul li a")
    product_category = product_detail_list[1].get_text(strip=True)
    product_description = detail_soup.select_one(".product-text").get_text(strip=True)

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
    response = session.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    product_list = soup.select(".product-item-content")
    product_image_list = soup.select(".product-item-image a")

    with futures.ThreadPoolExecutor(max_workers=10) as executor:
        products = tqdm(
            executor.map(scrape, product_list, product_image_list),
            total=len(product_list),
        )

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
