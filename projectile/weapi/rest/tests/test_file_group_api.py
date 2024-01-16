from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateGroupFileTest(BaseAPITestCase):
    """Test case for Product file endpoints"""

    def setUp(self):
        # Inherit from base setUp method
        super(PrivateGroupFileTest, self).setUp()

        # Send a POST request to the ListCreateAPIView with the data for a new group instance
        self.group_response = self.client.post(
            urlhelpers.group_list_url(), payloads.group_payload_one()
        )
        
        # Assert that the response status code is correct
        self.assertEqual(self.group_response.status_code, status.HTTP_201_CREATED)

        # File item payload
        self.payload = payloads.file_item_payload(payloads.generate_test_doc_file())

        # Send a POST request to the ListCreateAPIView with the data for a group file item  instance
        self.group_file_response = self.client.post(
            urlhelpers.group_file_list_url(self.group_response.data["uid"]),
            self.payload,
            type="multipart",
        )

    def test_group_file_create(self):
        # Test group file create api

        response = self.group_file_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], self.payload["status"])

    def test_group_file_list(self):
        # Test get group file list api

        get_response = self.client.get(
            urlhelpers.group_file_list_url(self.group_response.data["uid"])
        )
        
        # Assert that the response are correct
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["count"], 1)

    def test_group_file_detail(self):
        # Test group file detail api

        response = self.client.get(
            urlhelpers.group_file_detail_url(
                self.group_response.data["uid"], self.group_file_response.data["uid"]
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.payload["name"])

    def test_group_file_delete(self):
        # Test group file delete api

        response = self.client.delete(
            urlhelpers.group_file_detail_url(
                self.group_response.data["uid"], self.group_file_response.data["uid"]
            )
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
