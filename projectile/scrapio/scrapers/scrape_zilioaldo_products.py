import logging

from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

from scrapio.models import ScrapProductData


# Initialize the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

"""In development server, download the webdriver using the url https://chromedriver.chromium.org/downloads and add the driver path on your system ENV"""
"""In the deployment server, the webdriver and web binary must be installed in cloud storage and provide the path of driver and binary"""

# Initialize the webdriver
driver = webdriver.Chrome()

url = "https://www.zilioaldo.it/en/collection"

list_of_products = []


def scraping(url):
    # Navigate to the website
    driver.get(url)

    # Get the page source and create a BeautifulSoup object
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    organization = soup.find("title").get_text(strip=True).split("|")[1].strip()
    all_category = soup.select(".productFilters__item")[1:]

    for category in all_category:
        logging.info(category.text.strip())
        category_name = category.find("a").get_text().rstrip("0123456789")
        category_link = category.find("a")["href"]
        driver.get(category_link)
        lxml = driver.page_source
        product_soup = BeautifulSoup(lxml, "html.parser")
        all_product = product_soup.select(".productGrid__col")

        for product in tqdm(all_product):
            product_title = product.find("a", class_="productItem__title").get_text()
            image_link = product.find("img")["src"]
            product_link = product.find("a", class_="productItem__title")["href"]
            driver.get(product_link)
            description_soup = BeautifulSoup(driver.page_source, "html.parser")
            all_description = description_soup.find(
                "div", class_="container productDescription productDescription--left"
            )
            product_discription = " ".join(
                [
                    description.get_text().replace("\xa0", " ")
                    for description in all_description.find_all("p")
                ]
            )
            # Create product dictionary to load the data into database
            product_dict = {
                "title": product_title,
                "description": product_discription,
                "image_link": image_link,
                "product_link": product_link,
                "category": category_name,
                "organization": organization,
            }
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
    scraping(url)
    load_data_to_database(list_of_products)
    # Close the webdriver
    driver.quit()
