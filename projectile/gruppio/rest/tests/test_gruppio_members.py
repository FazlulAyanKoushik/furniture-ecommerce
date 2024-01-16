from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class GlobalMembersApiTests(BaseAPITestCase):
    """Test Group Members endpoints"""

    def setUp(self):
        super(GlobalMembersApiTests, self).setUp()

        # Create group
        self.group = self.client.post(
            we_urlhelpers.group_list_url(), payloads.group_payload_one()
        )

        # Assert that the response is correct
        self.assertEqual(self.group.status_code, status.HTTP_201_CREATED)

        # Create group member
        self.post_response = self.client.post(
            we_urlhelpers.member_list_url(self.group.data["uid"]),
            payloads.member_payload(self.user.slug),
        )

        # Assert that the response is correct
        self.assertEqual(self.group.status_code, status.HTTP_201_CREATED)

    def test_get_group_member_list(self):
        # Test get group member list api

        response = self.client.get(
            urlhelpers.group_member_list_url(self.group.data["slug"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["status"],
            payloads.member_payload(self.user.slug)["status"],
        )

    def test_get_group_member_detail(self):
        # Test get group member detail api

        response = self.client.get(
            urlhelpers.group_member_detail_url(
                self.group.data["slug"], self.post_response.data["uid"]
            )
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], self.post_response.data["role"])
