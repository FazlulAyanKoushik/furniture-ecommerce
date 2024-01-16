from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class GlobalGroupApiTest(BaseAPITestCase):
    """Test group api"""

    def setUp(self):
        super(GlobalGroupApiTest, self).setUp()

        # Create geoup
        self.group_response = self.client.post(
            we_urlhelpers.group_list_url(), payloads.group_payload_one()
        )

        # Assert that the response is correct
        self.assertEqual(self.group_response.status_code, status.HTTP_201_CREATED)

    def test_group_list(self):
        # Test get group list api

        response = self.client.get(urlhelpers.group_list_url())

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_group_detail(self):
        # Test get group detail api

        response = self.client.get(
            urlhelpers.group_detail_url(self.group_response.data["slug"])
        )

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the returned data is correct
        self.assertEqual(response.data["kind"], self.group_response.data["kind"])
