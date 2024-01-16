import tempfile

from PIL import Image

from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads as we_payloads
from weapi.rest.tests import urlhelpers as we_urlhelpers

from . import payloads, urlhelpers


class PublicOrganizationImageTest(BaseAPITestCase):
    """Test case for getting Organization Image"""

    def setUp(self):
        super(PublicOrganizationImageTest, self).setUp()

        # send a POST request to the ListCreateAPIView with the data for a new product instance
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

    def test_organization_image_list(self):
        """Test for getting organization image list"""

        # get organization images
        response = self.client.get(
            urlhelpers.organization_image_list_url(self.organization_slug)
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_organization_image_detail(self):
        """Test for retrieving organization image details"""

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            # media image payload
            payload = we_payloads.media_image_payload(image_file)

            # send a POST request to the ListCreateAPIView with the data for a new media image  instance
            image_response = self.client.post(
                we_urlhelpers.we_product_image_list_url(
                    self.product_response.data["uid"]
                ),
                payload,
                type="multipart",
            )

            # get organization images
            response = self.client.get(
                urlhelpers.organization_image_detail_url(
                    self.organization_slug, image_response.data["uid"]
                )
            )

            """Assert image created"""
            self.assertEqual(image_response.status_code, status.HTTP_201_CREATED)

            # assert that the response status code is correct
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.assertEqual(response.data["caption"], image_response.data["caption"])
