import tempfile

from PIL import Image

from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads as we_payloads, urlhelpers as we_urlhelpers

from . import payloads, urlhelpers


class PublicFileItemTest(BaseAPITestCase):
    # Test for get file item list and details

    def setUp(self):
        super(PublicFileItemTest, self).setUp()

        # create a new product instance with payload
        self.product_response = self.client.post(
            urlhelpers.we_product_list_url(), payloads.product_payload()
        )
        self.assertEqual(self.product_response.status_code, status.HTTP_201_CREATED)

        # get user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # get organization_slug
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # create temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)

            # file item payload
            payload = we_payloads.file_item_payload(image_file)

            # create file item with we_api
            self.response_file_item = self.client.post(
                we_urlhelpers.product_file_list_url(self.product_response.data["uid"]),
                payload,
                format="multipart",
            )

    def test_get_file_item(self):
        # test get file item list
        response = self.client.get(
            urlhelpers.file_item_list_url(self.organization_slug)
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the response data is correct
        self.assertEqual(response.data["count"], 1)
        # assert that the response data is correct
        self.assertEqual(
            response.data["results"][0]["uid"], self.response_file_item.data["uid"]
        )

    def test_get_file_item_details(self):
        # test get file item details
        response = self.client.get(
            urlhelpers.file_item_detail_url(
                self.organization_slug, self.response_file_item.data["uid"]
            )
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the response data is correct
        self.assertEqual(response.data["name"], self.response_file_item.data["name"])
