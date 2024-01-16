""" Test cases for organizations API """

from rest_framework import status

from common.base_test import BaseAPITestCase

from accountio.choices import OrganizationStatus

from common.base_test import BaseAPITestCase

from . import urlhelpers


class PrivateOrganizationApiTest(BaseAPITestCase):
    """Test private authenticated API calls for organizations"""

    def setUp(self):
        super(PrivateOrganizationApiTest, self).setUp()

        # getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # update organization status
        payload = {"status": OrganizationStatus.ACTIVE}
        organization_update = self.client.patch(urlhelpers.we_detail_url(), payload)

        # organization_slug create
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]
        self.organization_name = self.organization.data["results"][0]["organization"][
            "name"
        ]

    def test_create_organization_onboard(self):
        """Test for creating organization onboard"""

        response = self.onboarding_response

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data)

    def test_get_organization_api(self):
        """Test get_organization list api"""

        # response get
        response = self.client.get(urlhelpers.organization_list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_retrieve_organization_api(self):
        """Test retrieve_organization api"""

        # test retrieve
        response = self.client.get(
            urlhelpers.organization_detail_url(self.organization_slug)
        )

        # checking
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.organization_name)
