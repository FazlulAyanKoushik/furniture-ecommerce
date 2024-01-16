""" Test cases for organizations API """

from rest_framework import status

from common.base_test import BaseAPITestCase

from accountio.choices import OrganizationStatus

from common.base_test import BaseAPITestCase

from weapi.rest.tests import urlhelpers as we_urlhelpers

from weapi.rest.tests import payloads as we_payloads

from . import urlhelpers


class OrganizationBrandApiTest(BaseAPITestCase):
    """Test organization brand API test"""

    def setUp(self):
        super(OrganizationBrandApiTest, self).setUp()

        # Getting user organization list
        self.organization = self.client.get(urlhelpers.me_organization_list_url())

        # Update organization status
        self.update_organization_payload = {
            "status": OrganizationStatus.ACTIVE,
            "kind": "SUPPLIER",
        }
        self.organization_update = self.client.patch(
            urlhelpers.we_detail_url(), self.update_organization_payload
        )

        # Get organization slug
        self.organization_slug = self.organization.data["results"][0]["organization"][
            "slug"
        ]

        # Create product brand
        self.create_product_brand = self.client.post(
            we_urlhelpers.user_organization_product_brand_url(),
            we_payloads.product_brand_payload(),
        )

    def test_create_organization_brand(self):
        """Test for create organization brand"""

        response = self.create_product_brand

        # Assert that the response are correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["title"], we_payloads.product_brand_payload()["title"]
        )

    def test_get_organization_brand(self):
        """Test for get organization brand"""

        # Get organization brands
        response = self.client.get(
            urlhelpers.organization_brand_url(self.organization_slug)
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["results"][0]["title"],
            we_payloads.product_brand_payload()["title"],
        )
