import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from tqdm import tqdm

from ..models import ScrapProductData

url = "https://lanabgroup.se"


def scrape_product(product):
    with requests.Session() as session:
        if product.select_one("h3"):
            product_link = url + product["href"]
            product_category = product_link.split("/")[-3].replace("-", " ").title()

            product_title = product.select_one("h3").get_text()
            product_image_link = url + product.select_one(".lazy")["data-original"]
            product_organization = "Lanab Group"
            product_description = ""

            detail_response = session.get(product_link)
            detail_soup = BeautifulSoup(detail_response.content, "lxml")
            description = detail_soup.select(".productTopInfoWrapper p")

            if description:
                product_description = description[-1].get_text(strip=True)

            return {
                "title": product_title,
                "description": product_description,
                "image_link": product_image_link,
                "product_link": product_link,
                "category": product_category,
                "organization": product_organization,
            }
        else:
            return None


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


def main_boat():
    with requests.Session() as session:
        response = session.get(url)
        soup = BeautifulSoup(response.content, "lxml")

        product_list = soup.select(".productCatNav li a")

        list_of_products = []
        for product in product_list:
            product_link = url + product["href"]
            product_response = session.get(product_link)
            product_soup = BeautifulSoup(product_response.content, "lxml")
            products = product_soup.select(".col-md-12 ul li a")

            list_of_products.extend(products)

        with ThreadPoolExecutor(max_workers=10) as executor:
            scraped_products = executor.map(scrape_product, list_of_products)

        valid_products = [
            product for product in scraped_products if product is not None
        ]
        load_data_to_database(valid_products)
