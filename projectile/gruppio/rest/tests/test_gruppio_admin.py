from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class GlobalGroupAdminApiTest(BaseAPITestCase):
    def setUp(self):
        super(GlobalGroupAdminApiTest, self).setUp()

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

    def test_get_admin_list(self):
        response = self.client.get(
            urlhelpers.group_admin_list_url(self.group.data["slug"])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
