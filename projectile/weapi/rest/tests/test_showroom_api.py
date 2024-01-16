import tempfile

from PIL import Image

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateShowroomApiTests(BaseAPITestCase):
    def setUp(self):
        super(PrivateShowroomApiTests, self).setUp()

        with tempfile.NamedTemporaryFile(suffix=".jpg") as self.image_file:
            img = Image.new("RGB", (10, 10))
            img.save(self.image_file, format="JPEG")
            self.image_file.seek(0)

            payload = payloads.media_image_payload(self.image_file)

            self.showroom_response = self.client.post(
                urlhelpers.get_showroom_list_url(),
                payload,
                type="multipart",
            )
            self.assertEqual(
                self.showroom_response.status_code, status.HTTP_201_CREATED
            )

    def test_create_showroom_list(self):
        response = self.showroom_response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_showroom_list(self):
        response = self.client.get(urlhelpers.get_showroom_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["caption"],
            payloads.media_image_payload(self.image_file)["caption"],
        )

    def test_get_showroom_detail(self):
        response = self.client.get(
            urlhelpers.get_showroom_detail_url(self.showroom_response.data["uid"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["caption"], self.showroom_response.data["caption"]
        )

    def test_update_showroom_detail(self):
        payload = {
            "width": 20,
            "height": 10,
            "caption": "BMW",
            "copyright": "Bbmw",
            "priority": 2,
        }
        response = self.client.patch(
            urlhelpers.get_showroom_detail_url(self.showroom_response.data["uid"]),
            payload,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["copyright"], payload["copyright"])

    def test_delete_showroom(self):
        response = self.client.delete(
            urlhelpers.get_showroom_detail_url(self.showroom_response.data["uid"])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
