import logging

import csv
import os

from django.core.management.base import BaseCommand, CommandError

import pandas as pd

from ...models import PotentialLead

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        path = os.path.abspath(os.path.dirname(__file__))
        df = pd.read_excel(f"{path}/sff-leads.xlsx")
        print(df)
        items = []
        for index, row in df.iterrows():
            try:
                print(row["Name"])
                print(row["Address"])
                print(row["Postal Code / Area"])
                print(row["Phone"])
                print(row["Country"])
                print(row["Email"])
                print(row["Link"])
                pl = PotentialLead(
                    name=row["Name"],
                    address=row["Address"],
                    postal_code=row["Postal Code / Area"],
                    phone=row["Phone"],
                    country=row["Country"],
                    email=row["Email"],
                    website=row["Web"],
                    source_url=row["Link"],
                )
                items.append(pl)
            except Exception as e:
                logger.exception(e)
                logger.info(row)
                continue
        PotentialLead.objects.bulk_create(items)
