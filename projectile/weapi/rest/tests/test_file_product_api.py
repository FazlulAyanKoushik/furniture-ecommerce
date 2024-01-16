from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateProductFileTest(BaseAPITestCase):
    """Test case for Product file endpoints"""

    def setUp(self):
        # Inherit from base setUp method
        super(PrivateProductFileTest, self).setUp()

        # Send a POST request to the ListCreateAPIView with the data for a new product instance
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        # File item payload
        self.payload = payloads.file_item_payload(payloads.generate_test_doc_file())

        # Send a POST request to the ListCreateAPIView with the data for a new file item  instance
        self.product_file_response = self.client.post(
            urlhelpers.product_file_list_url(self.product_response.data["uid"]),
            self.payload,
            type="multipart",
        )

    def test_product_file_create(self):
        # Test product file create api

        response = self.product_file_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], self.payload["status"])

    def test_product_list(self):
        # Test product list

        get_response = self.client.get(
            urlhelpers.product_file_list_url(self.product_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 1)

    def test_product_file_detail(self):
        # Test product file detail

        response = self.client.get(
            urlhelpers.product_file_detail_url(
                self.product_response.data["uid"],
                self.product_file_response.data["uid"],
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["kind"], self.product_file_response.data["kind"])

    def test_product_file_delete(self):
        # Test product file delete api

        response = self.client.delete(
            urlhelpers.product_file_detail_url(
                self.product_response.data["uid"],
                self.product_file_response.data["uid"],
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
