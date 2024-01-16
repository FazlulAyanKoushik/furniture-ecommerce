import tempfile

from rest_framework import status

from common.base_test import BaseAPITestCase

from PIL import Image

from . import payloads, urlhelpers


class PrivateOrganizationImageTest(BaseAPITestCase):
    """Test case for Organization Image"""

    def setUp(self):
        super(PrivateOrganizationImageTest, self).setUp()

        payload = payloads.product_payload()

        # send a POST request to the ListCreateAPIView with the data for a new product instance
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payload
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

    def test_organization_image_list(self):
        """Test for getting organization image list"""

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = payloads.media_image_payload(image_file)

            # create product image
            product_response = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                payload,
                type="multipart",
            )
            self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

            # send a GET request to the ListCreateAPIView for MediaImage List
            response = self.client.get(urlhelpers.image_list_url())

            # assert that the response status code is correct
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # assert that the returned data is correct
            self.assertEqual(response.data["count"], 1)

    def test_retrieve_organization_image(self):
        """Test for retrieving organization image"""

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = payloads.media_image_payload(image_file)

            # create product image
            product_response = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                payload,
                type="multipart",
            )
            self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

            # send a GET request to the RetrieveUpdateDestroyAPIView for an individual MediaImage instance
            response = self.client.get(
                urlhelpers.image_detail_url(uid=product_response.data["uid"]),
                payload,
            )
            # assert that the response status code is correct
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # assert that the returned data is correct
            self.assertEqual(response.data["height"], product_response.data["height"])

    def test_update_organization_image(self):
        """Test for updating organization image"""

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = payloads.media_image_payload(image_file)

            # create product image
            product_response = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                payload,
                type="multipart",
            )
            self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

            # data update payload
            update_payload = {"height": 50}

            # send a P request to the RetrieveUpdateDestroyAPIView for an individual media image instance
            response = self.client.patch(
                urlhelpers.image_detail_url(uid=product_response.data["uid"]),
                update_payload,
            )
            # assert that the response status code is correct
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_image(self):
        """Test for deleting organization image"""

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            payload = payloads.media_image_payload(image_file)

            # create product image
            product_response = self.client.post(
                urlhelpers.we_product_image_list_url(self.product_response.data["uid"]),
                payload,
                type="multipart",
            )
            self.assertEqual(product_response.status_code, status.HTTP_201_CREATED)

            # send a DELETE request to the RetrieveUpdateDestroyAPIView for an individual MediaImage
            response = self.client.delete(
                urlhelpers.image_detail_url(uid=product_response.data["uid"])
            )

            # assert that the response status code is correct
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
