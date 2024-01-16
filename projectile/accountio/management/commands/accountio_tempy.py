import random
import string

from django.core.management.base import BaseCommand

from leadio.choices import PotentialLeadStatus
from leadio.models import PotentialLead

from accountio.models import Organization
from accountio.choices import OrganizationStatus

# a function that generates a random no that starts with 1111-ABCD
def generate_random_no():
    return "111111-" + "".join(random.choice(string.ascii_uppercase) for _ in range(4))


country_mapper = {
    "Australien": "au",
    "Belgien": "be",
    "Danmark": "dk",
    "Estland": "ee",
    "Finland": "fi",
    "Frankrike": "fr",
    "Italien": "it",
    "Kanada": "ca",
    "Kina": "cn",
    "Kroatien": "hr",
    "Lettland": "lv",
    "Litauen": "lt",
    "Nederländerna": "nl",
    "Norge": "no",
    "Polen": "pl",
    "Portugal": "pt",
    "Slovakien": "sk",
    "Spanien": "es",
    "Storbritannien": "gb",
    "Sverige": "se",
    "Sydkorea": "kr",
    "Tjeckien": "cz",
    "Tyskland": "de",
    "Ungern": "hu",
    "USA": "us",
}


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):
        leads = PotentialLead.objects.exclude(status=PotentialLeadStatus.CLOSED)
        for lead in leads:
            org, created = Organization.objects.get_or_create(name=lead.name)
            org.address = lead.address
            org.email = lead.email
            org.website_url = lead.website
            org.phone = lead.phone
            org.postal_area = lead.postal_area
            org.postal_code = lead.postal_code
            org.status = OrganizationStatus.PLACEHOLDER
            org.registration_no = generate_random_no()
            try:
                org.country = country_mapper[lead.country]
            except KeyError:
                pass
            org.save_dirty_fields()
