"""
Test cases for organizations group API
"""
from rest_framework import status

from common.base_test import BaseAPITestCase

from weapi.rest.tests import payloads, urlhelpers as we_urlhelpers

from . import urlhelpers


class PrivateOrganizationGroupApiTest(BaseAPITestCase):
    """Test class for testing authenticated api call on Organizations Group"""

    def setUp(self):
        super(PrivateOrganizationGroupApiTest, self).setUp()

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())
        self.organization_slug = self.organization.data["results"][0]["organization"]["slug"]

        # Create new organization group
        self.organization_group = self.client.post(
            we_urlhelpers.group_list_url(), payloads.group_payload_one()
        )

        # assert that the response status code is correct
        self.assertEqual(self.organization_group.status_code, status.HTTP_201_CREATED)

    def test_retrieving_organization_groups(self):
        """Test retrieving groups that belong to a organization"""

        # response of retrieving groups
        response = self.client.get(
            urlhelpers.organization_group_list_url(self.organization_slug)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["name"], self.organization_group.data["name"]
        )

    def test_organization_group_detail(self):
        """Test get single group under organization and group slug"""

        # response of retrieving organization group detail
        response = self.client.get(
            urlhelpers.organization_group_detail_url(
                self.organization_slug, self.organization_group.data["slug"]
            )
        )

        # response testing
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.organization_group.data["name"])
