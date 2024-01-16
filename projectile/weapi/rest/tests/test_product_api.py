from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationProductAPIViewTests(BaseAPITestCase):
    """Test case for creating products from weapi app"""

    def setUp(self):
        super(PrivateOrganizationProductAPIViewTests, self).setUp()

        # posting new product
        self.post_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_create_product(self):
        """Test for creating product"""

        response = self.post_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payloads.product_payload()["title"])

    def test_get_product_list(self):
        """Test for getting product list"""

        # retrieving product list
        response = self.client.get(urlhelpers.we_product_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_update_product(self):
        """Test for updating product"""

        payload = {"title": "Updated By Staff"}

        response = self.client.patch(
            urlhelpers.we_product_detail_url(self.post_response.data["uid"]), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_delete_product(self):
        """Test for deleting product"""

        response = self.client.delete(
            urlhelpers.we_product_detail_url(self.post_response.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_create_with_brand(self):
        product_brand = self.client.post(
            urlhelpers.user_organization_product_brand_url(),
            payloads.product_brand_payload(),
        )
        self.assertEqual(product_brand.status_code, status.HTTP_201_CREATED)

        payload = payloads.product_payload_with_brand(product_brand.data["uid"])
        response = self.client.post(urlhelpers.we_product_list_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_update_with_brand(self):

        product_brand = self.client.post(
            urlhelpers.user_organization_product_brand_url(),
            payloads.product_brand_payload(),
        )
        self.assertEqual(product_brand.status_code, status.HTTP_201_CREATED)

        payload = {"title": "Updated By Staff", "brand": product_brand.data["uid"]}

        response = self.client.patch(
            urlhelpers.we_product_detail_url(self.post_response.data["uid"]), payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])
