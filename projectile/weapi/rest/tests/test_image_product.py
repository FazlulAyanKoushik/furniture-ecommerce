import os

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateProductImageTest(BaseAPITestCase):
    """Test Case for Creating Product Image"""

    def setUp(self):
        super(PrivateProductImageTest, self).setUp()

        # Create a new product instance
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        # Create a temporary image file
        self.image_file = payloads.generate_test_image()
        self.image_file_2 = payloads.generate_test_image()

        # Open temporary image file
        with open(self.image_file, "rb") as data:
            # Media image payload
            self.payload = payloads.media_image_payload(data)

            # Create a new product image instance
            self.post_response = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                self.payload,
                type="multipart",
            )

        # creating 2nd image for product
        with open(self.image_file_2, "rb") as data:
            # Media image payload
            self.payload_2 = payloads.media_image_payload(data)

            # Create a new product image instance
            self.post_response_2 = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                self.payload_2,
                type="multipart",
            )

    def tearDown(self):
        os.remove(self.image_file)

    def test_create_product_image(self):
        # Test create product image api

        response = self.post_response

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["priority"], self.payload["priority"])

    def test_product_image_list(self):
        # Test get product image list api

        response = self.client.get(
            urlhelpers.we_product_image_list_url(self.product_response.data["uid"])
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["images"][0]["caption"], self.post_response.data["caption"]
        )

    def test_get_product_image_detail(self):
        # Test get product image detail api

        response = self.client.get(
            urlhelpers.we_product_image_detail_url(
                self.product_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["priority"], self.payload["priority"])

    def test_update_product_image(self):
        # Test update project image detail api

        # Payload for update project image
        update_payload = {"caption": "BMW Updated", "copyright": "BMW Updated"}

        response = self.client.patch(
            urlhelpers.we_product_image_detail_url(
                self.product_response.data["uid"],
                self.post_response.data["uid"],
            ),
            update_payload,
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption"], update_payload["caption"])

    def test_product_image_delete(self):
        # Test delete product image api

        response = self.client.delete(
            urlhelpers.we_product_image_detail_url(
                self.product_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the responses is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_product_cover_image(self):
        # Test to set cover image for a product
        payload = {"image": self.post_response_2.data["uid"]}

        response = self.client.patch(
            urlhelpers.we_product_set_cover_image_url(
                self.product_response.data["uid"], self.post_response_2.data["uid"]
            ),
            payload,
        )
        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["priority"], self.payload["priority"])
