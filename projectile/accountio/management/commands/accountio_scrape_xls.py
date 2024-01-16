import logging


import os
import math

from datetime import date

import pandas as pd
from tqdm import tqdm

from django.core.management.base import BaseCommand

from accountio.models import Organization

logger = logging.getLogger(__name__)


def replace_nan_with_empty_string(d):
    return {
        k: "" if (isinstance(v, str) and v.lower() == "nan") or math.isnan(v) else v
        for k, v in d.items()
    }


class Command(BaseCommand):
    help = "Parse Excel file and store data in a Django JSONField"

    def handle(self, *args, **options):
        path = os.path.abspath(os.path.dirname(__file__))
        file_path = f"{path}/Supplers_SNI_7410_SE_230522.xlsx"
        df = pd.read_excel(file_path)
        df = df.fillna("")

        today = date.today().strftime("%Y%m%d")

        for index, row in tqdm(df.iterrows()):
            try:
                data = {
                    "COMPANY_NAME": row["COMPANY_NAME"],
                    "ORG_NO": row["ORG_NO"],
                    "VAT_NO": row["VAT_NO"],
                    "POSTAL_ADDRESS": row["POSTAL_ADDRESS"],
                    "ZIPCODE": row["ZIPCODE"],
                    "CITY": row["CITY"],
                    "COUNTYNAME": row["COUNTYNAME"],
                    "COUNTRY": row["COUNTRY"],
                    "TELEPHONE": row["TELEPHONE"],
                    "WWW": row["WWW"] if row["WWW"] != "Nan" else "",
                    "MANAGING_DIRECTOR": row["MANAGING_DIRECTOR"],
                    "MANAGING_DIRECTOR_EMAIL": row["MANAGING_DIRECTOR_EMAIL"],
                    "MARKETING_DIRECTOR": row["MARKETING_DIRECTOR"],
                    "MARKETING_DIRECTOR_EMAIL": row["MARKETING_DIRECTOR_EMAIL"],
                    "FINANCIAL_DIRECTOR": row["FINANCIAL_DIRECTOR"],
                    "FINANCIAL_DIRECTOR_EMAIL": row["FINANCIAL_DIRECTOR_EMAIL"],
                    "TECHNICAL_DIRECTOR": row["TECHNICAL_DIRECTOR"],
                    "TECHNICAL_DIRECTOR_EMAIL": row["TECHNICAL_DIRECTOR_EMAIL"],
                    "PURCHASING_DIRECTOR": row["PURCHASING_DIRECTOR"],
                    "PURCHASING_DIRECTOR_EMAIL": row["PURCHASING_DIRECTOR_EMAIL"],
                    "PERSONNEL_DIRECTOR": row["PERSONNEL_DIRECTOR"],
                    "PERSONNEL_DIRECTOR_EMAIL": row["PERSONNEL_DIRECTOR_EMAIL"],
                    "IT_MANAGER": row["IT_MANAGER"],
                    "IT_MANAGER_EMAIL": row["IT_MANAGER_EMAIL"],
                    "SALES_MANAGER": row["SALES_MANAGER"],
                    "SALES_MANAGER_EMAIL": row["SALES_MANAGER_EMAIL"],
                    "PRODUCTION_MANAGER": row["PRODUCTION_MANAGER"],
                    "PRODUCTION_MANAGER_EMAIL": row["PRODUCTION_MANAGER_EMAIL"],
                    "PR_MANAGER": row["PR_MANAGER"],
                    "PR_MANAGER_EMAIL": row["PR_MANAGER_EMAIL"],
                    "ACTIVITY_CODE_1": row["ACTIVITY_CODE_1"],
                    "ACTIVITY_CODE_1_DESCRIPTION": row["ACTIVITY_CODE_1_DESCRIPTION"],
                    "ACTIVITY_CODE_2": row["ACTIVITY_CODE_2"],
                    "FISCAL_YEAR_1": row["FISCAL_YEAR_1"],
                    "REVENUES_YEAR_1": row["REVENUES_YEAR_1"],
                    "RESULT_YEAR_1": row["RESULT_YEAR_1"],
                    "EMPLOYEES_TOTAL_YEAR_1": row["EMPLOYEES_TOTAL_YEAR_1"],
                }

                org = Organization()
                org.name = data["COMPANY_NAME"]
                org.display_name = (
                    data["COMPANY_NAME"]
                    .replace(" AB", "")
                    .replace(" ApS", "")
                    .replace(" A/S", "")
                    .replace(" Oy", "")
                )
                org.registration_no = data.get("ORG_NO")
                org.vat_no = data.get("VAT_NO", "")
                org.email = (
                    data.get("MANAGING_DIRECTOR_EMAIL")
                    or data.get("MARKETING_DIRECTOR_EMAIL")
                    or data.get("PURCHASING_DIRECTOR_EMAIL")
                    or data.get("SALES_MANAGER_EMAIL")
                    or ""
                )
                org.phone = data.get("TELEPHONE", "")
                org.address = data.get("POSTAL_ADDRESS", "")
                org.postal_code = data.get("ZIPCODE", "")
                org.city = data.get("CITY", "")
                org.county = data.get("COUNTYNAME", "")
                org.country = data["COUNTRY"].lower()
                org.scraped = data
                org.segment = "interior-designer"
                org.kind = "SERVICE_PROVIDER"
                org.status = "PLACEHOLDER"
                org.source = f"NMD-{today}"
                if "74103" in [data["ACTIVITY_CODE_1"], data["ACTIVITY_CODE_2"]]:
                    org.save()
                    logger.info(f"Added organization {org.name} successfully!")
            except Exception as e:
                logger.exception(e)
                continue


"""
for org in orgs:
    email = org.website_url.replace("http://www.", "info@")
    email = email.split("/")[0]
    try:
        org.email = email
        org.save(update_fields=["email"])
    except Exception as e:
        print(e)
        continue  

for org in orgs:
    if www and len(www) > 0:
        if "://" not in www:
            www = f"http://{www}"
            try:
                org.website_url = www
                org.save(update_fields=["website_url"])
            except Exception as e:
                print(e)
                continue
"""
