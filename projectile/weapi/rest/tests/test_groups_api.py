from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateGroupApiTest(BaseAPITestCase):
    """Test private group api"""

    def setUp(self):
        super(PrivateGroupApiTest, self).setUp()

        # Create group
        self.group_response = self.client.post(
            urlhelpers.group_list_url(), payloads.group_payload_one()
        )

    def test_create_group(self):
        # Test create group api

        response = self.group_response

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payloads.group_payload()["name"])

    def test_get_group_list(self):
        # Test get group list api

        response = self.client.get(urlhelpers.group_list_url())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_group_detail(self):
        # Test get group detail api

        response = self.client.get(
            urlhelpers.group_detail_url(group_uid=self.group_response.data["uid"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], self.group_response.data["status"])

    def test_update_group_detail(self):
        # Test update group detail api

        payload = {"name": "Group Name Updated"}

        response = self.client.patch(
            urlhelpers.group_detail_url(self.group_response.data["uid"]), payload
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], response.data["name"])

    def test_delete_group_detail(self):
        # Test delete group details api

        response = self.client.delete(
            urlhelpers.group_detail_url(self.group_response.data["uid"])
        )

        # Assert that the response is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_group_with_invite_members(self):
        """Test for invite group members while creating group"""

        response = self.client.get(
            urlhelpers.member_list_url(self.group_response.data["uid"])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_create_group_with_invite_new_members(self):
        """Test for creating new users and invite for group members while creating group"""

        # Create geoup
        group_response = self.client.post(
            urlhelpers.group_list_url(), payloads.group_payload_two()
        )

        # assert that the response status code is correct
        self.assertEqual(group_response.status_code, status.HTTP_201_CREATED)

        first_name = payloads.group_payload_two()["first_name"].lower()

        member_response = self.client.get(
            urlhelpers.member_list_url(group_response.data["uid"])
        )

        self.assertEqual(member_response.status_code, status.HTTP_200_OK)
        self.assertEqual(member_response.data["count"], 1)
        self.assertIn(first_name, member_response.data["results"][0]["user"])
