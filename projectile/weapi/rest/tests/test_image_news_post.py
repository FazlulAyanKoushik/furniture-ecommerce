from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers

from PIL import Image
import tempfile


class PrivateNewsPostImageTest(BaseAPITestCase):
    """TestCase for creating News Post Image"""

    def setUp(self):
        super(PrivateNewsPostImageTest, self).setUp()

        # Create a news post instance
        self.create_post_response = self.client.post(
            urlhelpers.news_list_url(), payloads.news_payload()
        )
        self.assertEqual(self.create_post_response.status_code, status.HTTP_201_CREATED)

        # Create a temporary image file
        self.image_file = payloads.generate_test_image()

        # Media image payload
        self.post_image_payload = payloads.media_image_payload(self.image_file)

        # Open temporary image file
        with tempfile.NamedTemporaryFile(suffix=".jpg") as self.image_file:
            img = Image.new("RGB", (10, 10))
            img.save(self.image_file, format="JPEG")

            # generating a image file
            self.image_file.seek(0)
            self.post_response = self.client.post(
                urlhelpers.we_news_post_image_list_url(
                    self.create_post_response.data["uid"]
                ),
                payloads.media_image_payload(self.image_file),
                type="multipart",
            )

    def test_create_news_image(self):
        # Test create news image api

        response = self.post_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["priority"], self.post_image_payload["priority"]
        )

    def test_get_news_image_list(self):
        # Test get news image list api

        response = self.client.get(
            urlhelpers.we_news_post_image_list_url(
                self.create_post_response.data["uid"]
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_news_image_detail(self):
        # Test get news image detail api

        response = self.client.get(
            urlhelpers.we_news_post_image_detail_url(
                self.create_post_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["kind"], self.post_response.data["kind"])

    def test_delete_news_image(self):
        # Test delete news image api

        response = self.client.delete(
            urlhelpers.we_news_post_image_detail_url(
                self.create_post_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
