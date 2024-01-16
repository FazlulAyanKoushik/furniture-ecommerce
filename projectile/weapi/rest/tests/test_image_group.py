import os

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateGroupImageTest(BaseAPITestCase):
    """Test for Group Image API"""

    def setUp(self):
        super(PrivateGroupImageTest, self).setUp()

        # Create a new group instance
        self.create_group_response = self.client.post(
            urlhelpers.group_list_url(), payloads.group_payload_one()
        )
        # Assert that the response is correct
        self.assertEqual(
            self.create_group_response.status_code, status.HTTP_201_CREATED
        )

        # Create a temporary image file
        self.image_file = payloads.generate_test_image()

        # Open temporary image file
        with open(self.image_file, "rb") as data:
            # Media image payload
            self.payload = payloads.media_image_payload(data)

            # Create a new group image instance
            self.post_response = self.client.post(
                urlhelpers.we_group_image_list_url(
                    self.create_group_response.data["uid"]
                ),
                self.payload,
                type="multipart",
            )

    def tearDown(self):
        os.remove(self.image_file)

    def test_group_image_create(self):
        # Test create group image api

        response = self.post_response

        # Assert that the response are correct
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["priority"], self.payload["priority"])

    def test_group_image_list(self):
        # Test get group image list api

        response = self.client.get(
            urlhelpers.we_group_image_list_url(self.create_group_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_group_image_detail(self):
        # Test get group image detail api

        response = self.client.get(
            urlhelpers.we_group_image_detail_url(
                self.create_group_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["kind"], self.payload["kind"])

    def test_update_group_image(self):
        # Test update group image api

        # Payload for update group image
        update_payload = {"caption": "BMW Updated", "copyright": "BMW Updated"}

        response = self.client.patch(
            urlhelpers.we_group_image_detail_url(
                self.create_group_response.data["uid"], self.post_response.data["uid"]
            ),
            update_payload,
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption"], update_payload["caption"])

    def test_delete_group_image(self):
        # Test delete group image api

        response = self.client.delete(
            urlhelpers.we_group_image_detail_url(
                self.create_group_response.data["uid"], self.post_response.data["uid"]
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
