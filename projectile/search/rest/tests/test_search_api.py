from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads, urlhelpers


class PublicSearhApiTest(BaseAPITestCase):
    """Test private group api tests"""

    def setUp(self):
        super(PublicSearhApiTest, self).setUp()

    def test_search_organization_list(self):
        """Test for searh organization list"""

        response = self.client.get("/api/v1/search/organizations?name=Tesla")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_product_list(self):
        """Test for searching product list"""

        payload = payloads.product_payload()
        product_response = self.client.post(urlhelpers.we_product_list_url(), payload)

        self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/v1/search/products?title=Tesla Model-3")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
