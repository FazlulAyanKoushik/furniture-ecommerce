# import logging
# import requests

# from bs4 import BeautifulSoup
# from selenium import webdriver
# from tqdm import tqdm

# from scrapio.models import ScrapProductData


# # Initialize the logger
# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )

# """Download webdriver using the url https://chromedriver.chromium.org/downloads and add the driver path on your system ENV"""

# # Initialize the webdriver
# driver = webdriver.Chrome(executable_path='/home/bappi/Supplers/supplers-backend/chromedriver')


# url_list = [
#     "https://www.isku.com/global/en/products/storaging",
#     "https://www.isku.com/global/en/products/tables-desks",
#     "https://www.isku.com/global/en/products/space-within-a-space",
#     "https://www.isku.com/global/en/products/sofas-easy-chairs",
#     "https://www.isku.com/global/en/products/space-dividers-panels",
#     "https://www.isku.com/global/en/products/accessories",
#     "https://www.isku.com/global/en/products/chairs",
#     "https://www.isku.com/global/en/products/stools-pouffes",
#     "https://www.isku.com/global/en/products/myflow-family",
#     "https://www.isku.com/global/en/products/control-room-solutions",
#     "https://www.isku.com/global/en/products/control-room-consoles",
# ]

# list_of_products = []


# def scraping(url):
#     # Navigate to the website
#     driver.get(url)

#     # Get the page source and create a BeautifulSoup object
#     html = driver.page_source
#     soup = BeautifulSoup(html, "html.parser")

#     # Get products
#     product_data = soup.find_all("li", class_="category-item")

#     # Get products data
#     for product in tqdm(product_data):
#         # Print progress report
#         logging.info(product.text.strip())
#         # Base url for product link
#         base_url = "https://www.isku.com"
#         # Products data
#         category = soup.find("h1", class_="category-name").text.strip()
#         image_link = product.find("img", class_="product-image")["src"]
#         if image_link.startswith("//"):
#             image_link = "https:" + image_link
#         product_link = (
#             f"{base_url}" + product.find("a", class_="product-item-link")["href"]
#         )
#         # Get products detail data
#         product_description = ""
#         description_response = requests.get(product_link)
#         description_soup = BeautifulSoup(description_response.text, "html.parser")
#         description = description_soup.find_all(
#             "div", class_="description-text md2html-text"
#         )
#         if description:
#             product_description = description[0].text.strip().replace("\n", ". ")
#         product_title = description_soup.find("h1", class_="product-name")
#         if product_title:
#             title = product_title.text.strip()
#         product_organization = description_soup.find_all(
#             "div", class_="product-short-desciption"
#         )
#         for data in product_organization:
#             organization = data.find_all("span")[-1].text.strip()

#         # Create product dictionary to load data into database
#         product_dict = {
#             "title": title,
#             "description": product_description,
#             "image_link": image_link,
#             "product_link": product_link,
#             "organization": organization,
#             "category": category,
#         }
#         # Append data into the list_of_products
#         list_of_products.append(product_dict)


# # Load the scraped data into the database
# def load_data_to_database(list_of_products):
#     logging.info("Loading scraped products into the database !")
#     ScrapProductData.objects.bulk_create(
#         [
#             ScrapProductData(
#                 title=item["title"],
#                 description=item["description"],
#                 image_link=item["image_link"],
#                 product_link=item["product_link"],
#                 organization=item["organization"],
#                 category=item["category"],
#             )
#             for item in tqdm(list_of_products)
#             if not ScrapProductData.objects.filter(
#                 product_link=item["product_link"]
#             ).exists()
#         ]
#     )


# # Create a function to call in management command
# def main_bot():
#     for url in url_list:
#         scraping(url)
#     load_data_to_database(list_of_products)
#     # Close the webdriver
#     driver.quit()