import requests
from bs4 import BeautifulSoup
from concurrent import futures
from functools import partial
from tqdm import tqdm

from ..models import ScrapProductData


url = "https://skipperfurniture.se/home/mobler/"


def scrape(product, category_name):
    try:
        product_link = product["href"]
    except:
        product_link = None

    if product_link:
        product_image_link = product.select_one("img")["src"]
        product_response = session.get(product_link)
        product_soup = BeautifulSoup(product_response.content, "lxml")
        product_title = product_soup.select_one(".vc_custom_heading").get_text()
        product_description = product_soup.select_one(".wpb_wrapper p").get_text()
        product_category = category_name
        product_organization = "Skipper Furniture"

        return (
            product_title,
            product_description,
            product_image_link,
            product_link,
            product_category,
            product_organization,
        )
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


def main_bot():
    global session
    session = requests.Session()
    response = session.get(url)

    soup = BeautifulSoup(response.content, "lxml")

    category_soup = soup.select(".wpb_wrapper h2 a")

    for category in category_soup:
        category_name = category.get_text(strip=True)
        category_url = category["href"]
        category_response = session.get(category_url)
        category_soup = BeautifulSoup(category_response.content, "lxml")
        product_list = category_soup.select(
            ".vc_single_image-wrapper.vc_box_border_grey"
        )

        partial_scrape = partial(scrape, category_name=category_name)

        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            products = executor.map(partial_scrape, product_list)

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
            if product is not None
        ]

        load_data_to_database(list_of_products)

    session.close()
