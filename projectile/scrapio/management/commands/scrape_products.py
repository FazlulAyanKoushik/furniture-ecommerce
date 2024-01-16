from django.core.management.base import BaseCommand

from scrapio.scrapers import (
    scrape_bisley_products,
    scrape_blastation_products,
    scrape_dalform_products,
    scrape_normann_copenhagen_products,
    scrape_essem_products,
    scrape_globalstole_products,
    scrape_hermanmiller_products,
    # scrape_isku_products,
    scrape_lundbergs_products,
    scrape_lanabgroup_products,
    scrape_oblure_products,
    scrape_phone_alone_products,
    scrape_piudesign_products,
    scrape_skargaarden_products,
    scrape_skipper_furniture_products,
    # scrape_zilioaldo_products,
)


class Command(BaseCommand):
    help = "Command to scrape products and save into the database"

    def handle(self, *args, **kwargs):
        # scrape_bisley_products.main_bot()
        print("Scraping Norman Copenhagen products...")
        # scrape_normann_copenhagen_products.main_bot()
        print("Scraping Bla Station products...")
        scrape_blastation_products.main_bot()
        scrape_dalform_products.main_bot()
        scrape_essem_products.main_bot()
        scrape_globalstole_products.main_bot()
        scrape_hermanmiller_products.main_bot()
        # scrape_isku_products.main_bot()          # Selenium
        scrape_lundbergs_products.main_bot()
        scrape_lanabgroup_products.main_boat()
        scrape_oblure_products.main_bot()
        scrape_phone_alone_products.main_bot()
        scrape_piudesign_products.main_bot()
        scrape_skargaarden_products.main_bot()
        scrape_skipper_furniture_products.main_bot()
        # scrape_zilioaldo_products.main_bot()     # Selenium
