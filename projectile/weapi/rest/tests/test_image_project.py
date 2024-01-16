import os

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateOrganizationProjectImageTests(BaseAPITestCase):
    """Tests for specific organization news"""

    # Override setUp method
    def setUp(self):
        super(PrivateOrganizationProjectImageTests, self).setUp()

        # Create a new project instance
        self.project_create_response = self.client.post(
            urlhelpers.project_list_url(), payloads.project_payload()
        )
        self.assertEqual(
            self.project_create_response.status_code, status.HTTP_201_CREATED
        )

        # Create a temporary image file
        self.image_file = payloads.generate_test_image()
        self.image_file_2 = payloads.generate_test_image()

        # Open temporary image file
        with open(self.image_file, "rb") as data:
            # Media image payload
            self.payload = payloads.media_image_payload(data)

            # Create a new project image instance
            self.project_image_response = self.client.post(
                urlhelpers.we_project_image_list_url(
                    self.project_create_response.data["uid"]
                ),
                self.payload,
                type="multipart",
            )

        with open(self.image_file_2, "rb") as data:
            # Media image payload
            self.payload_2 = payloads.media_image_payload(data)

            # Create a new project image instance
            self.project_image_response_2 = self.client.post(
                urlhelpers.we_project_image_list_url(
                    self.project_create_response.data["uid"]
                ),
                self.payload_2,
                type="multipart",
            )

    def tearDown(self):
        os.remove(self.image_file)

    def test_create_project_image(self):
        # Test create project image api

        response = self.project_image_response

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["priority"], self.payload["priority"])

    def test_get_project_image_list(self):
        # Test get project image list api

        response = self.client.get(
            urlhelpers.we_project_image_list_url(
                self.project_create_response.data["uid"]
            )
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["images"][0]["caption"], self.payload["caption"] )

       
    def test_get_project_image_detail(self):
        # Test get project image detail api

        response = self.client.get(
            urlhelpers.project_image_detail_url(
                self.project_create_response.data["uid"],
                self.project_image_response.data["uid"],
            )
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["priority"], self.payload["priority"])

    def test_update_project_image(self):
        # Test update project image detail api

        # Payload for update project image
        update_payload = {"caption": "BMW Updated", "copyright": "BMW Updated"}

        response = self.client.patch(
            urlhelpers.project_image_detail_url(
                self.project_create_response.data["uid"],
                self.project_image_response.data["uid"],
            ),
            update_payload,
        )

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["caption"], update_payload["caption"])

    def test_delete_project_image(self):
        # Test delete project image api

        response = self.client.delete(
            urlhelpers.project_image_detail_url(
                self.project_create_response.data["uid"],
                self.project_image_response.data["uid"],
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_set_project_cover_image(self):
        # Test set project cover image

        payload = {"image": self.project_image_response_2.data["uid"]}       

        response = self.client.patch(
            urlhelpers.we_project_set_cover_image_url(
                self.project_create_response.data["uid"],
                self.project_image_response_2.data["uid"]
            ), 
            payload
        )

        get_image_response = self.client.get(
            urlhelpers.we_project_image_list_url(self.project_create_response.data["uid"])
        )    

        # Assert that the responses are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_image_response.data["cover_image"]["uid"], payload["image"])