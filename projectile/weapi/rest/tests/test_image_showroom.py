import os
import tempfile

from PIL import Image

from rest_framework import status

from common.base_test import BaseAPITestCase


from . import payloads, urlhelpers


class PrivateShowroomImageTest(BaseAPITestCase):
    def setUp(self):
        super(PrivateShowroomImageTest, self).setUp()

        with tempfile.NamedTemporaryFile(suffix=".jpg") as self.image_file:
            img = Image.new("RGB", (10, 10))
            img.save(self.image_file, format="JPEG")
            self.image_file.seek(0)

            payload = payloads.media_image_payload(self.image_file)

            self.create_showroom_response = self.client.post(
                urlhelpers.get_showroom_list_url(),
                payload,
                type="multipart",
            )

            self.assertEqual(
                self.create_showroom_response.status_code, status.HTTP_201_CREATED
            )

    def test_get_showroom_image_list(self):
        response = self.client.get(
            urlhelpers.we_showroom_image_list_url(
                self.create_showroom_response.data["uid"]
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_set_showroom_cover_image(self):
        response = self.client.patch(
            urlhelpers.we_set_showroom_cover_image_url(
                self.create_showroom_response.data["uid"],
                self.create_showroom_response.data["uid"],
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
