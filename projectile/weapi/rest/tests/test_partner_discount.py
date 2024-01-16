from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PartnerDiscountTestCase(BaseAPITestCase):
    def setUp(self):
        # Inherit from base setUp method
        super(PartnerDiscountTestCase, self).setUp()

        # Create partner
        with open(payloads.generate_test_xlsx_file().name, "rb") as f:
            self.bulk_partners_response = self.client.post(
                urlhelpers.we_partners_bulk_create_url(),
                {"partner_list": f},
                format="multipart",
            )

        # Get partner partner list
        self.partner_list_response = self.client.get(urlhelpers.we_partners_list_url())

        # Get partner uid
        self.partner_uid = self.partner_list_response.data["results"][0]["uid"]

        # Create partner discount
        self.partner_discount_response = self.client.post(
            urlhelpers.we_partners_discount_url(self.partner_uid),
            payloads.create_product_discount_payload(),
        )

    def test_create_partner_discount(self):
        # Test partner discount create

        # Partner discount create response
        response = self.partner_discount_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["kind"], payloads.create_product_discount_payload()["kind"]
        )

    def test_get_partner_discount_list(self):
        # Test partner discount list

        # Get partner discount list
        response = self.client.get(urlhelpers.we_partner_discount_list_url())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["category"],
            payloads.create_product_discount_payload()["category"],
        )
