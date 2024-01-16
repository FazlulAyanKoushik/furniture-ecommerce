from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateTagsTest(BaseAPITestCase):
    def setUp(self):
        super(PrivateTagsTest, self).setUp()

        # Create service(after creating the service, a tag will be created automatically)
        self.create_service_response = self.client.post(
            urlhelpers.we_services_list_url(), payloads.service_payload()
        )

    def test_create_tags(self):
        """Test creating tags"""

        response = self.create_service_response

        # Assert that the status code is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tags(self):
        """Test get tags"""

        response = self.client.get(urlhelpers.tag_url_list())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], payloads.service_payload()["name"]
        )

    def test_update_tags(self):
        """Test creating tags"""
        post_response = self.client.post(
            urlhelpers.tag_url_list(), payloads.tag_payload()
        )
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        payload = {"name": "Update"}
        response = self.client.patch(
            urlhelpers.tag_url_detail(post_response.data["uid"]), payload
        )

        # Assert that the response is correct
        self.assertEqual(response.data["name"], payload["name"])

    def test_delete_tags(self):
        """Test creating tags"""
        post_response = self.client.post(
            urlhelpers.tag_url_list(), payloads.tag_payload()
        )

        # Assert that the response is correct
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(
            urlhelpers.tag_url_detail(post_response.data["uid"])
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
