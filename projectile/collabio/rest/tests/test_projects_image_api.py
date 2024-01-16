import os

from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import urlhelpers as we_urlhelpers, payloads as we_payloads

from . import urlhelpers, payloads


class GlobalProjectDetailImageListTest(BaseAPITestCase):
    # Override setUp method
    def setUp(self):
        super(GlobalProjectDetailImageListTest, self).setUp()

        # Create a new project instance
        self.project_create_response = self.client.post(
            we_urlhelpers.project_list_url(), payloads.project_payload()
        )
        self.assertEqual(
            self.project_create_response.status_code, status.HTTP_201_CREATED
        )

        self.image_file = we_payloads.generate_test_image()

        # Open temporary image file
        with open(self.image_file, "rb") as data:
            # Media image payload
            self.payload = we_payloads.media_image_payload(data)

            # Create a new project image instance
            self.project_image_response = self.client.post(
                we_urlhelpers.we_project_image_list_url(
                    self.project_create_response.data["uid"]
                ),
                self.payload,
                type="multipart",
            )

    def tearDown(self):
        os.remove(self.image_file)

    def test_get_global_project_image_list(self):
        response = self.client.get(
            urlhelpers.public_project_detail_image_list_url(
                self.project_create_response.data["slug"]
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
