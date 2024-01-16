from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateBulkCreatePartnerApiTest(BaseAPITestCase):
    """Test Private Partner Bulk_Create Api"""

    def setUp(self):
        super(PrivateBulkCreatePartnerApiTest, self).setUp()

    def test_create_partners_with_bulk_create(self):
        # Test private bulk create partners api

        # Open the temporary file and post it to the API endpoint
        with open(payloads.generate_test_xlsx_file().name, "rb") as f:
            response = self.client.post(
                urlhelpers.we_partners_bulk_create_url(),
                {"partner_list": f},
                format="multipart",
            )

            # Assert that the response is correct
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
