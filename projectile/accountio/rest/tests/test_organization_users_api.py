# Test Case for Organization Users

from rest_framework import status

from common.base_test import BaseAPITestCase

from . import urlhelpers


class OrganizationProductRestApiTest(BaseAPITestCase):
    def setUp(self):
        super(OrganizationProductRestApiTest, self).setUp()

        # get user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # organization slug
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # get organization user
        self.organization_user = self.client.get(
            urlhelpers.organization_user_list_url(self.organization_slug)
        )
        self.assertEqual(self.organization_user.status_code, status.HTTP_200_OK)

    def test_get_organization_user(self):
        # test get organization user
        response = self.organization_user

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the response data is correct
        self.assertEqual(response.data["count"], 1)

    def test_get_organization_user_details(self):
        # test response user retrieve

        # get organization user details
        response = self.client.get(
            urlhelpers.organizaion_user_detail_url(
                self.organization_slug,
                self.organization_user.data["results"][0]["user"]["slug"],
            )
        )

        # assert that the response status code is correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that the response data is correct
        self.assertEqual(
            response.data["uid"], self.organization.data["results"][0]["uid"]
        )
