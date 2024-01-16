import tempfile

from rest_framework import status

from common.base_test import BaseAPITestCase

from PIL import Image

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class PrivateProductImageApiTests(BaseAPITestCase):
    def setUp(self):
        super(PrivateProductImageApiTests, self).setUp()

        # send a POST request to the ListCreateAPIView with the data for a new product instance
        self.product_response = self.client.post(
            we_urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        self.product_slug = self.product_response.data["slug"]

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = payloads.media_image_payload(image_file)

            self.post_response = self.client.post(
                we_urlhelpers.we_product_image_list_url(
                    self.product_response.data["uid"]
                ),
                payload,
                type="multipart",
            )
            self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

    def test_product_image_list(self):
        """Test for gettting product image list"""

        response = self.client.get(urlhelpers.product_image_list_url(self.product_slug))

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the returned data is correct
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_product_image(self):
        """Test for retrieving product image detail"""

        image_uid = self.post_response.data["uid"]
        image_caption = self.post_response.data["caption"]

        response = self.client.get(
            urlhelpers.product_image_detail_url(self.product_slug, image_uid)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption"], image_caption)
