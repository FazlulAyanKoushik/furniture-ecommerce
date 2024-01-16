from rest_framework import status

from common.base_test import BaseAPITestCase

from . import payloads, urlhelpers


class PrivateMembersApiTest(BaseAPITestCase):
    """Test Members endpoint tests"""

    def setUp(self):
        super(PrivateMembersApiTest, self).setUp()

        # Create group
        self.group = self.client.post(
            urlhelpers.group_list_url(), payloads.group_payload_one()
        )

        # Assert that the response is correct
        self.assertEqual(self.group.status_code, status.HTTP_201_CREATED)

        # Create group member
        self.member_response = self.client.post(
            urlhelpers.member_list_url(self.group.data["uid"]),
            payloads.member_payload(self.user.slug),
        )
        # Assert that the response is correct
        self.assertEqual(self.member_response.status_code, status.HTTP_201_CREATED)

    def test_create_member(self):
        # Test create group member api

        response = self.member_response

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # assert that the returned data is correct
        self.assertEqual(
            response.data["role"], payloads.member_payload(self.user.slug)["role"]
        )

    def test_get_member_list(self):
        # Test get group member list api

        # send a GET request to the ListCreateAPIView with the data for a new member instance
        response = self.client.get(urlhelpers.member_list_url(self.group.data["uid"]))

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["status"], self.member_response.data["status"])

    def test_get_group_member_detail(self):
        # Test get group member detail api

        # send a GET request to the ListCreateAPIView with the data for a new member instance
        response = self.client.get(
            urlhelpers.member_detail_url(
                group_uid=self.group.data["uid"],
                member_uid=self.member_response.data["uid"],
            )
        )
        
        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], self.member_response.data["role"])

    def test_update_member(self):
        # Test for update group member api

        # Update field payload
        payload = {"role": "MODERATOR"}

        # send a PATCH request to the RetrieveUpdateDestroyAPIView with updated data for an individual member
        patch_response = self.client.patch(
            urlhelpers.member_detail_url(
                group_uid=self.group.data["uid"],
                member_uid=self.member_response.data["uid"],
            ),
            payload,
        )
        # Assert that the response are correct
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        
        response = self.client.get(
            urlhelpers.member_detail_url(
                group_uid=self.group.data["uid"],
                member_uid=self.member_response.data["uid"],
            ),
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["role"], response.data["role"])
        self.assertEqual(patch_response.data, response.data)

    def test_delete_member(self):
        # Test delete group member api

        # send a DELETE request to the RetrieveUpdateDestroyAPIView for an individual member
        response = self.client.delete(
            urlhelpers.member_detail_url(
                group_uid=self.group.data["uid"],
                member_uid=self.member_response.data["uid"],
            ),
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
