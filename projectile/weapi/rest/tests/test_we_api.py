from rest_framework import status

from common.base_test import BaseAPITestCase

from . import urlhelpers, payloads


class PrivateOrganizationAPIViewTests(BaseAPITestCase):
    """Test case for we newsdesk"""

    def setUp(self):
        super(PrivateOrganizationAPIViewTests, self).setUp()

    def test_retrieve_default_organization(self):
        """Test to retrieve default organization information"""

        response = self.client.get(urlhelpers.we_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["name"],
            payloads.organization_onboard_payload()["organization_name"],
        )

    def test_update_we_information(self):
        """Test to update default organization information"""

        # Payload for update
        payload = {"email": "mossaddak@gmail.com"}

        response = self.client.patch(urlhelpers.we_url(), payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], payload["email"])
